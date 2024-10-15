import pandas as pd
import dask.dataframe as dd

from .base_source import DataSource

class MarketData(DataSource):
    def __init__(self, stock_name, datetime_range, columns):
        self.stock_name = stock_name
        self.datetime_range = datetime_range
        self.columns = columns
        self.data = None

    def load_data(self):
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

    def downsample(self, rule='1s', agg_func='mean'):
        self.data = self.data.resample(rule).agg(agg_func)
