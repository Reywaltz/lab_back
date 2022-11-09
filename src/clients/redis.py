from abc import ABCMeta, abstractclassmethod, abstractmethod


class BaseClient(metaclass=ABCMeta):
    @abstractclassmethod
    def create(cls):
        pass

    @abstractmethod
    def close(self):
        pass
