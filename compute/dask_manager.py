from dask.distributed import Client

class DaskManager:
    def __init__(self):
        self.client = Client(processes=True)

    def get_client(self):
        return self.client
