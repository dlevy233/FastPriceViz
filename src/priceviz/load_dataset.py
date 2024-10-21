import logging
from typing import List, Optional
from datetime import timedelta
import time
import hashlib
import json
from priceviz.types import TimeSeriesSource, DownsamplingStrategy, DataColumn, DownsamplingStrategyType
import dask.dataframe as dd
import pandas as pd
from dask.diagnostics.progress import ProgressBar
from priceviz.dask_utils import setup_dask_client
from priceviz.utils import suggest_resources
from diskcache import Cache
import pyarrow as pa
from pyarrow import parquet as pq
import pickle
from dask.distributed import performance_report
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the cache with 2GB of memory
cache = Cache(2e9)  # 2GB cache for global use
# Note: diskcache.Cache doesn't require registration

def is_parquet_file(filename: str) -> bool:
    return filename.lower().endswith('.parquet')

class DatasetLoader:
    def __init__(self, sources: List[TimeSeriesSource], granularity: timedelta,
                 downsampling_strategy: DownsamplingStrategy, name: str,
                 datetime_column: str = 'timestamp', chunk_size: str = '100MB'):
        self.sources = sources
        self.granularity = granularity
        self.downsampling_strategy = downsampling_strategy
        self.name = name
        self.datetime_column = datetime_column
        self.chunk_size = chunk_size
        self.cache = Cache("./dataset_cache")  # Create a persistent cache

    def _generate_cache_key(self) -> str:
        # Create a unique key based on input parameters
        key_data = {
            "sources": [s.filename for s in self.sources],
            "granularity": str(self.granularity),
            "downsampling_strategy": self.downsampling_strategy.strategy,
            "name": self.name,
            "datetime_column": self.datetime_column,
            "chunk_size": self.chunk_size
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_total_source_size(self) -> int:
        total_size = 0
        for source in self.sources:
            if os.path.isdir(source.filename):
                for root, _, files in os.walk(source.filename):
                    for file in files:
                        if is_parquet_file(file):
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)
            elif os.path.isfile(source.filename) and is_parquet_file(source.filename):
                total_size += os.path.getsize(source.filename)
            else:
                logger.warning(f"Skipping unknown file type: {source.filename}")
        return total_size

    def load_and_compute(self) -> Optional[pd.DataFrame]:
        cache_key = self._generate_cache_key()

        try:
            # Try to get the result from cache
            if cache_key in self.cache:
                cached_result = pickle.loads(self.cache[cache_key])
                logger.info(f"Returning cached result for dataset '{self.name}'")
                return cached_result

            # If not in cache, compute and store the result
            with setup_dask_client(
                n_workers=4,
                threads_per_worker=2,
                memory_limit='2GB'
            ) as client:
                start_time = time.time()

                # Calculate original dataset size
                original_size = self._get_total_source_size()

                # Load and downsample the dataset
                dataset = self._load_dataset()
                if dataset is None:
                    logger.error(f"Failed to load dataset '{self.name}'")
                    return None

                downsampling_time = time.time() - start_time

                # Compute the dataset
                with ProgressBar(), performance_report(filename="dask-report.html"):
                    computed_dataset = dataset.compute()

                computation_time = time.time() - start_time - downsampling_time

                self._log_summary(computed_dataset, original_size)
                self._log_performance(downsampling_time, computation_time)

                # Store the result in cache
                self.cache[cache_key] = pickle.dumps(computed_dataset)

                return computed_dataset
        except Exception as e:
            logger.error(f"Critical error in load_and_compute for dataset '{self.name}': {str(e)}", exc_info=True)
            return None

    def _load_dataset(self) -> Optional[dd.DataFrame]:
        try:
            downsampled_data = []
            for source in self.sources:
                df = self._load_and_downsample_source(source)
                downsampled_data.append(df)

            combined_df = dd.concat(downsampled_data, axis=0)
            return combined_df
        except Exception as e:
            logger.error(f"Error in _load_dataset for '{self.name}': {str(e)}")
            return None

    def _load_and_downsample_source(self, source: TimeSeriesSource) -> dd.DataFrame:
        df = dd.read_parquet(source.filename, blocksize=self.chunk_size)
        df[self.datetime_column] = dd.to_datetime(df[self.datetime_column])
        df = df.set_index(self.datetime_column, sorted=True)
        downsampled = self._apply_downsampling(df)
        downsampled['ticker'] = source.ticker
        # Add a check here
        if 'ticker' not in downsampled.columns:
            logger.warning(f"'ticker' column not added for source {source.ticker}")
        return downsampled

    def _apply_downsampling(self, df: dd.DataFrame) -> dd.DataFrame:
        strategies = {
            "average_pooling": "mean",
            "max_pooling": "max",
            "min_pooling": "min",
            "median_pooling": "median",
        }

        if self.downsampling_strategy.strategy not in strategies:
            raise ValueError(f"Unsupported downsampling strategy: {self.downsampling_strategy.strategy}")

        resample_method = strategies[self.downsampling_strategy.strategy]

        numeric_columns = df.select_dtypes(include=['number']).columns
        non_numeric_columns = df.select_dtypes(exclude=['number']).columns

        downsampled_numeric = df[numeric_columns].resample(self.granularity).agg(resample_method)
        downsampled_non_numeric = df[non_numeric_columns].resample(self.granularity).first()

        return dd.concat([downsampled_numeric, downsampled_non_numeric], axis=1)

    def _log_summary(self, df: pd.DataFrame, original_size: int):
        downsampled_size = df.memory_usage(deep=True).sum()
        num_rows, num_cols = df.shape

        logger.info(
            f"Dataset '{self.name}' loaded:\n"
            f"  Original size: {format_size(original_size)}\n"
            f"  Downsampled size: {format_size(downsampled_size)}\n"
            f"  Compression ratio: {original_size / downsampled_size:.2f}x\n"
            f"  Rows: {num_rows:,}\n"
            f"  Columns: {num_cols}\n"
            f"  Sources: {len(self.sources)}\n"
            f"  Granularity: {self.granularity}\n"
            f"  Strategy: {self.downsampling_strategy.strategy}"
        )

    def _log_performance(self, downsampling_time: float, computation_time: float):
        total_time = downsampling_time + computation_time
        logger.info("\n" + "="*50)
        logger.info("Performance Summary:")
        logger.info(f"{'Downsampling:':<20} {downsampling_time:.2f}s ({downsampling_time/total_time:.1%})")
        logger.info(f"{'Computation:':<20} {computation_time:.2f}s ({computation_time/total_time:.1%})")
        logger.info(f"{'Total Time:':<20} {total_time:.2f}s")
        logger.info("="*50)

def load_dataset(*args, **kwargs) -> Optional[pd.DataFrame]:
    loader = DatasetLoader(*args, **kwargs)
    return loader.load_and_compute()

def load_source(source: TimeSeriesSource, datetime_column: str, chunk_size: str) -> dd.DataFrame:
    df = dd.read_parquet(source.filename, blocksize=chunk_size)

    if datetime_column not in df.columns:
        raise ValueError(f"Missing datetime column '{datetime_column}' in source: {source.ticker}")

    df[datetime_column] = dd.to_datetime(df[datetime_column])
    return df.set_index(datetime_column, sorted=True)

def apply_downsampling(df: dd.DataFrame, strategy: DownsamplingStrategy, granularity: timedelta) -> dd.DataFrame:
    strategies = {
        "average_pooling": "mean",
        "max_pooling": "max",
        "min_pooling": "min",
        "median_pooling": "median",
    }

    if strategy.strategy not in strategies:
        raise ValueError(f"Unsupported downsampling strategy: {strategy.strategy}")

    resample_method = strategies[strategy.strategy]

    numeric_columns = df.select_dtypes(include=['number']).columns
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns

    downsampled_numeric = df[numeric_columns].resample(granularity).agg(resample_method)
    downsampled_non_numeric = df[non_numeric_columns].resample(granularity).first()

    return dd.concat([downsampled_numeric, downsampled_non_numeric], axis=1)

def format_size(size_bytes: float) -> str:
    """Format size in bytes to the most appropriate unit."""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
    return f"{size_bytes:.2f} {units[unit_index]}"
