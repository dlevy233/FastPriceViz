import pandas as pd
import dask.dataframe as dd
from .base_source import DataSource
from collections import OrderedDict

class MarketData(DataSource):
    # Class-level cache
    _cache = OrderedDict()
    _cache_size = 5  # Number of items to keep in cache

    def __init__(self, stock_name, datetime_range, columns):
        self.stock_name = stock_name
        self.datetime_range = datetime_range
        self.columns = columns
        self.data = None

    def load_data(self):
        cache_key = (self.stock_name, self.datetime_range)
        if cache_key in self._cache:
            self.data = self._cache[cache_key]
            # Move accessed item to the end (most recently used)
            self._cache.move_to_end(cache_key)
        else:
            # Path to Parquet files
            path = f'data/market/{self.stock_name}/*.parquet'
            # Read data with specified columns, including 'timestamp'
            self.data = dd.read_parquet(path, columns=self.columns + ['timestamp'])
            # Set 'timestamp' as index
            self.data = self.data.set_index('timestamp', sorted=True)
            # Ensure the index is timezone-aware
            self.data.index = self.data.index.map_partitions(
                lambda idx: idx.tz_convert('America/New_York')
            )
            # Create timezone-aware start and end timestamps
            start = pd.Timestamp(self.datetime_range[0], tz='America/New_York')
            end = pd.Timestamp(self.datetime_range[1], tz='America/New_York')
            # Filter by datetime_range
            self.data = self.data.loc[start:end]

            # Add to cache
            self._cache[cache_key] = self.data
            if len(self._cache) > self._cache_size:
                # Remove the least recently used item
                self._cache.popitem(last=False)

    def downsample(self, rule='1s', agg_func='mean'):
        self.data = self.data.resample(rule).agg(agg_func)

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    @classmethod
    def set_cache_size(cls, size):
        cls._cache_size = size
        # Trim cache if necessary
        while len(cls._cache) > cls._cache_size:
            cls._cache.popitem(last=False)
