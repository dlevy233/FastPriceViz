import pandas as pd
import dask.dataframe as dd
from .base_source import DataSource

class MarketData(DataSource):
    def __init__(self, stock_name, datetime_range, columns, **kwargs):
        super().__init__(stock_name, f'data/market/{stock_name}/*.parquet', datetime_range, columns, **kwargs)

    def load_data(self, resolution='1s'):
        self.data = self._read_and_process_data(resolution)
        return self.data

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

    def get_data(self, columns=None, resolution='1s', view_range=None):
        if view_range:
            resolution = self._calculate_adaptive_resolution(view_range)
        return super().get_data(columns, resolution, view_range)

class BucketedDataFromObjectStore(DataSource):
    def load_data(self, resolution='1s'):
        data = self._read_and_process_data(resolution)
        # Add any specific processing for bucketed data here
        return data

class CustomDataFromObjectStore(DataSource):
    def __init__(self, name, filename, datetime_range, columns, custom_processing=None, **kwargs):
        super().__init__(name, filename, datetime_range, columns, **kwargs)
        self.custom_processing = custom_processing

    def load_data(self, resolution='1s'):
        data = self._read_and_process_data(resolution)
        if self.custom_processing:
            data = self.custom_processing(data)
        return data
