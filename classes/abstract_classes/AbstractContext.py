from abc import *

class AbstractContext(metaclass=ABCMeta):
    @abstractmethod
    def write(self, key: str, val: str):
        pass

    @abstractmethod
    def get_keys(self) -> str:
        pass

    def get_vals(self) -> list:
        pass