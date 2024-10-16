import unittest
import pandas as pd
from data.sources.market_data import MarketData
from dask_expr import DataFrame as DaskDataFrame

class TestMarketData(unittest.TestCase):
    def setUp(self):
        self.start_time = '2024-05-01 09:30:00'
        self.end_time = '2024-05-01 09:40:00'
        self.columns = ['price']
        self.market_data = MarketData('AAPL', (self.start_time, self.end_time), self.columns)

    def test_load_data(self):
        self.market_data.load_data()
        self.assertIsNotNone(self.market_data.data)
        self.assertIsInstance(self.market_data.data, DaskDataFrame)

    def test_get_data(self):
        data = self.market_data.get_data()
        self.assertIsInstance(data, DaskDataFrame)
        self.assertEqual(list(data.columns), self.columns)

    def test_downsample(self):
        self.market_data.load_data(resolution='1s')
        original_data = self.market_data.data
        self.market_data.downsample(rule='5s')
        self.assertNotEqual(len(original_data.compute()), len(self.market_data.data.compute()))

    def test_cache(self):
        # Clear cache before testing
        MarketData.clear_cache()

        # Load data twice
        self.market_data.load_data()
        cache_size_before = len(MarketData._cache)
        self.market_data.load_data()
        cache_size_after = len(MarketData._cache)

        # Cache size should not increase on second load
        self.assertEqual(cache_size_before, cache_size_after)

    def test_different_resolutions(self):
        data_1s = self.market_data.get_data(resolution='1s')
        data_100ms = self.market_data.get_data(resolution='100ms')
        
        # The 100ms data should have more rows than the 1s data
        self.assertGreater(len(data_100ms.compute()), len(data_1s.compute()))

if __name__ == '__main__':
    unittest.main()
