import unittest
from compute.dask_manager import DaskManager
from dask.distributed import Client

class TestDaskManager(unittest.TestCase):
    def setUp(self):
        self.dask_manager = DaskManager()

    def test_client(self):
        client = self.dask_manager.get_client()
        self.assertIsNotNone(client)
        self.assertIsInstance(client, Client)

    def test_client_is_running(self):
        client = self.dask_manager.get_client()
        self.assertTrue(client.scheduler_info()['services'])

    def test_client_can_compute(self):
        client = self.dask_manager.get_client()
        future = client.submit(lambda x: x + 1, 10)
        result = future.result()
        self.assertEqual(result, 11)

if __name__ == '__main__':
    unittest.main()
