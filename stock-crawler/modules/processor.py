import os
import json
import time

from .crawler import crawl_stock_price
from .utils import convert_value_to_float, get_datetime_now_iso
from .logger import log

def get_stocks_names(__history_collection):
  data = []
  pipeline = [
    {
      '$group': {
        '_id': "$name",
        'name': { '$first': "$name" }
      }
    }, {
      '$project': {
        '_id': 0,
        'name': 1
      }
    }
  ]
  histories = __history_collection.aggregate(pipeline)
  for history in histories:
    data.append(history.get('name'))
  return data

def process(__http_client, __history_collection):
  while True:
    stocks = get_stocks_names(__history_collection)
    log(stocks)

    for stock in stocks:
      stock_price = crawl_stock_price(__http_client, stock)
      if stock_price is not None:
        stock_history = {
          'name': stock,
          'price': convert_value_to_float(stock_price),
          'date': get_datetime_now_iso()
        }
        log(stock_history)
        try:
          __history_collection.insert_one(stock_history)
        except Exception as e:
          log(e)
          continue

    # sleep 60 secs
    time.sleep(60)
