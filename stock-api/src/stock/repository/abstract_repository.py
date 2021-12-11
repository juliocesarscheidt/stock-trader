from abc import ABCMeta, abstractmethod


class AbstractRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_last_stock(self, args: dict) -> dict:
        raise ("Method not implemented")

    @abstractmethod
    def find_last_stocks(self, country=None) -> list:
        raise ("Method not implemented")
