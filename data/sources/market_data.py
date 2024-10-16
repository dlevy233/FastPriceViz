import pandas as pd
import dask.dataframe as dd
from .base_source import DataSource
from collections import OrderedDict

class MarketData(DataSource):
    # Class-level cache
    _cache = OrderedDict()
    _cache_size = 5  # Number of items to keep in cache
    _current_resolution = None

    def __init__(self, stock_name, datetime_range, columns):
        self.stock_name = stock_name
        self.datetime_range = datetime_range
        self.columns = columns
        self.data = None
        self.path = f'data/market/{self.stock_name}/*.parquet'

    def load_data(self, resolution='1s'):
        cache_key = (self.stock_name, self.datetime_range, tuple(self.columns), resolution)
        if cache_key in self._cache:
            self.data = self._cache[cache_key]
            # Move accessed item to the end (most recently used)
            self._cache.move_to_end(cache_key)
        else:
            # Read data with specified columns, including 'timestamp'
            self.data = dd.read_parquet(self.path, columns=self.columns + ['timestamp'])
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
            # Downsample data based on the requested resolution
            self.data = self.data.resample(resolution).mean()
            self._current_resolution = resolution
            
            # Add to cache
            self._cache[cache_key] = self.data
            if len(self._cache) > self._cache_size:
                # Remove the least recently used item
                self._cache.popitem(last=False)

    def get_data(self, columns=None, resolution='1s', view_range=None):
        if columns is None:
            columns = self.columns
        
        if view_range is not None:
            adaptive_resolution = self._calculate_adaptive_resolution(view_range)
            if self.data is None or self._current_resolution != adaptive_resolution:
                self.load_data(adaptive_resolution)
            data = self.data.loc[view_range[0]:view_range[1]]
        else:
            if self.data is None or self._current_resolution != resolution:
                self.load_data(resolution)
            data = self.data

        return data[columns]

    def _calculate_adaptive_resolution(self, view_range):
        view_duration = (view_range[1] - view_range[0]).total_seconds()
        if view_duration <= 60:  # 1 minute or less
            return '100ms'
        elif view_duration <= 300:  # 5 minutes or less
            return '500ms'
        elif view_duration <= 3600:  # 1 hour or less
            return '1s'
        elif view_duration <= 86400:  # 1 day or less
            return '1min'
        else:
            return '5min'

    def downsample(self, rule='1s', agg_func='mean'):
        if self.data is not None:
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
