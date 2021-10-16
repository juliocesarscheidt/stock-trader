import json
import pika

def publish(__channel, __message, __exchange, __routing_key=''):
  __channel.basic_publish(exchange=__exchange,
                          routing_key=__routing_key,
                          body=json.dumps(__message),
                          properties=pika.BasicProperties(
                            delivery_mode = 2,
                          ))
