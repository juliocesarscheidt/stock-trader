from abc import ABCMeta, abstractmethod


class AbstractMongo(metaclass=ABCMeta):
    @abstractmethod
    def get_client(self):
        raise ("Method not implemented")

    @abstractmethod
    def set_database(self, database=None):
        raise ("Method not implemented")
