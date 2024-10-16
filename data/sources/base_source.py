from abc import ABC, abstractmethod
from collections import OrderedDict
import pandas as pd
import dask.dataframe as dd

class DataSource(ABC):
    _cache = OrderedDict()
    _cache_size = 5

    def __init__(self, name, filename, datetime_range, columns, **kwargs):
        self.name = name
        self.filename = filename
        self.datetime_range = datetime_range
        self.columns = columns
        self.data = None
        self.additional_info = kwargs

    @abstractmethod
    def load_data(self, resolution='1s'):
        pass

    def get_data(self, columns=None, resolution='1s', view_range=None):
        if columns is None:
            columns = self.columns
        cache_key = (self.name, self.datetime_range, tuple(columns), resolution, view_range)
        if cache_key in self._cache:
            data = self._cache[cache_key]
            self._cache.move_to_end(cache_key)
        else:
            data = self.load_data(resolution)
            if view_range:
                data = data.loc[view_range[0]:view_range[1]]
            self._cache[cache_key] = data
            if len(self._cache) > self._cache_size:
                self._cache.popitem(last=False)
        return data[columns]

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    @classmethod
    def set_cache_size(cls, size):
        cls._cache_size = size
        while len(cls._cache) > cls._cache_size:
            cls._cache.popitem(last=False)

    def _read_and_process_data(self, resolution='1s'):
        data = dd.read_parquet(self.filename, columns=self.columns + ['timestamp'])
        data = data.set_index('timestamp', sorted=True)
        data.index = data.index.map_partitions(lambda idx: idx.tz_convert('America/New_York'))
        start = pd.Timestamp(self.datetime_range[0], tz='America/New_York')
        end = pd.Timestamp(self.datetime_range[1], tz='America/New_York')
        data = data.loc[start:end]
        return data.resample(resolution).mean()
