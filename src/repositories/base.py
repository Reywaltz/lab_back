from abc import ABCMeta, abstractmethod


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def set(self):
        raise NotImplementedError
