import os
import json
import pika
import time

from .crawler import crawl_stock_price
from .utils import get_datetime_now_iso, get_rabbitmq_channel
from .logger import log

RABBITMQ_URI = os.environ.get('RABBITMQ_URI')
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE')
RETRY_SECONDS = int(os.environ.get('RETRY_SECONDS', '30'))

def generate_callback(http_client, history_collection):
  def callback_queue(__channel, __method, __properties, __body):
    message = json.loads(__body)
    log(message)

    stock_name = message['name']
    stock_country = message['country']

    stock_price = crawl_stock_price(http_client, stock_country, stock_name)
    log('stock_price ' + str(stock_price))

    if stock_price is None:
      log('[INFO] No stock price found for ' + stock_name)
      __channel.basic_ack(delivery_tag=__method.delivery_tag)
    else:
      stock_history = {
        'name': stock_name,
        'country': stock_country,
        'price': stock_price,
        'date': get_datetime_now_iso()
      }
      log(stock_history)
      try:
        history_collection.insert_one(stock_history)
        __channel.basic_ack(delivery_tag=__method.delivery_tag)
      except Exception as e:
        log(e)
        # requeue message
        __channel.basic_nack(delivery_tag=__method.delivery_tag, multiple=False, requeue=True)

  return callback_queue

def start_consume(callback):
  try:
    channel = get_rabbitmq_channel(RABBITMQ_URI)
  except Exception as e:
    raise e
  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(
    queue=RABBITMQ_QUEUE, auto_ack=False, on_message_callback=callback
  )
  try:
    channel.start_consuming()
  except Exception as e:
    raise e

def consume(__http_client, __history_collection):
  callback = generate_callback(__http_client, __history_collection)
  while True:
    try:
      start_consume(callback)
      break
    except Exception as e:
      log(e)
      log('Waiting {} seconds before retry..'.format(RETRY_SECONDS))
      time.sleep(RETRY_SECONDS)
      continue
