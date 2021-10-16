import os
import json
import pika

from .crawler import crawl_stock_price
from .utils import convert_value_to_float, get_datetime_now_iso, get_rabbitmq_channel
from .logger import log

RABBITMQ_URI = os.environ.get('RABBITMQ_URI')
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE')

def generate_callback(http_client, history_collection):
  def callback_queue(__channel, __method, __properties, __body):
    message = json.loads(__body)
    log(message)

    stock_name = message['name']

    stock_price = crawl_stock_price(http_client, stock_name)
    if stock_price is not None:
      stock_history = {
        'name': stock_name,
        'price': convert_value_to_float(stock_price),
        'date': get_datetime_now_iso()
      }
      log(stock_history)
      history_collection.insert_one(stock_history)

    __channel.basic_ack(delivery_tag=__method.delivery_tag)
    log(' [x] Done')

  return callback_queue

def consume(__http_client, __history_collection):
  callback = generate_callback(__http_client, __history_collection)

  channel = get_rabbitmq_channel(RABBITMQ_URI)

  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(
      queue=RABBITMQ_QUEUE, auto_ack=False, on_message_callback=callback
  )
  channel.start_consuming()
