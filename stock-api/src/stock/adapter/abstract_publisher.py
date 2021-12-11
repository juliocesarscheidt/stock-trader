from abc import ABCMeta, abstractmethod


class AbstractPublisher(metaclass=ABCMeta):
    @abstractmethod
    def get_connection(self):
        raise ("Method not implemented")

    @abstractmethod
    def get_channel(self):
        raise ("Method not implemented")

    @abstractmethod
    def publish(self, __message, __exchange, __routing_key=""):
        raise ("Method not implemented")
