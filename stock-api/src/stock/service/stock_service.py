from stock.common.logger import log
from stock.config import get_rabbitmq_config
from stock.adapter.abstract_publisher import AbstractPublisher
from stock.adapter.publisher import RabbitmqPublisher
from stock.repository.abstract_repository import AbstractRepository
from stock.repository.stock_repository import StockRepository


class StockService:
    rabbitmq_config = get_rabbitmq_config()
    repository: AbstractRepository
    publisher: AbstractPublisher

    def __init__(self):
        self.repository = StockRepository()
        self.publisher = RabbitmqPublisher()

    def find_last_stock(self, args: dict) -> dict:
        data = self.repository.find_last_stock(args)

        if data is None:
            # publish to queue, to be crawled, only if there is a country specified
            if "country" not in args:
                return

            try:
                log("Publishing {}".format(str(args)))
                self.publisher.publish(
                    args,
                    self.rabbitmq_config["exchange"],
                    self.rabbitmq_config["routing_key"],
                )
            except Exception as e:
                log(e)
                return None

        return data

    def find_last_stocks(self, country=None) -> list:
        data = self.repository.find_last_stocks(country)
        return data
