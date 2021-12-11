import json
import pika

from stock.config import get_rabbitmq_config
from stock.common.logger import log
from stock.adapter.abstract_publisher import AbstractPublisher
from stock.common.utils import retry


class RabbitmqPublisher(AbstractPublisher):
    config = get_rabbitmq_config()
    connection = None
    channel = None

    def get_connection(self):
        if self.connection is not None:
            log("returning connection already opened")
            return self.connection

        params = pika.URLParameters(self.config["uri"])
        self.connection = pika.BlockingConnection(params)

    def get_channel(self):
        if self.channel is not None:
            log("returning channel already opened")
            return self.channel

        self.channel = self.connection.channel()

    def publish(self, __message, __exchange, __routing_key=""):
        def publish_callback():
            self.get_connection()
            self.get_channel()

            self.channel.basic_publish(
                exchange=__exchange,
                routing_key=__routing_key,
                body=json.dumps(__message),
                properties=pika.BasicProperties(delivery_mode=2,),
            )

        retry(publish_callback)
