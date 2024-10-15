from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def downsample(self, *args, **kwargs):
        pass
