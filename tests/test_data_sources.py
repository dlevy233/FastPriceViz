import unittest
from data.sources.market_data import MarketData

class TestMarketData(unittest.TestCase):
    def test_load_data(self):
        market_data = MarketData('AAPL', ('2024-05-01 09:30:00', '2024-05-01 09:40:00'), ['price'])
        market_data.load_data()
        self.assertIsNotNone(market_data.data)
