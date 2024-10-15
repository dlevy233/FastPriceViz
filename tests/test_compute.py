import unittest
from compute.dask_manager import DaskManager

class TestDaskManager(unittest.TestCase):
    def test_client(self):
        manager = DaskManager()
        client = manager.get_client()
        self.assertIsNotNone(client)
