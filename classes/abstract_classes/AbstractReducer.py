from abc import *
from classes.abstract_classes.AbstractContext import AbstractContext

class AbstractReducer(metaclass=ABCMeta):
    @abstractmethod
    def reduce(self, key: str, values: list, context: AbstractContext):
        pass