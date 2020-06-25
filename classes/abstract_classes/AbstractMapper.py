from abc import *
from classes.abstract_classes.AbstractContext import AbstractContext

class AbstractMapper(metaclass=ABCMeta):
    @abstractmethod
    def map(self, key: str, value: str, context: AbstractContext):
        pass