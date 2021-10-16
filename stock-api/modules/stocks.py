import os

from flask_restful import Resource
from flask import make_response, jsonify
from .logger import log
from .publisher import publish
from .utils import get_rabbitmq_channel

RABBITMQ_URI = os.environ.get('RABBITMQ_URI', 'amqp://dev:dev@rabbitmq/?heartbeat=30')
RABBITMQ_EXCHANGE = os.environ.get('RABBITMQ_EXCHANGE', 'stocks_queue_exchange')
RABBITMQ_ROUTING_KEY = os.environ.get('RABBITMQ_ROUTING_KEY', 'stocks_queue')

class Stock(Resource):
  def __init__(self, history_collection):
    self.history_collection = history_collection

  def get_last_stock_by_name(self, name: str):
    data = None
    # sort descending
    histories = self.history_collection.find({'name': name}).sort('date', -1).skip(0).limit(1)
    for history in histories:
      data = {
        'id': str(history.get('_id')),
        'name': history.get('name'),
        'price': history.get('price'),
        'date': history.get('date'),
      }
    if data is None:
      channel = get_rabbitmq_channel(RABBITMQ_URI)
      # publish to queue, to be crawled
      publish(channel, {'name': name}, RABBITMQ_EXCHANGE, RABBITMQ_ROUTING_KEY)
      return None
    return data

  def get_last_stocks(self):
    data = []
    # sort descending
    pipeline = [
      {
        '$sort': { 'date': -1 }
      }, {
        '$group': {
          '_id': "$name",
          'object_id': { '$first': "$_id" },
          'name': { '$first': "$name" },
          'price': { '$first': "$price" },
          'date': { '$first': "$date" }
        }
      }, {
        '$project': {
          '_id': "$object_id",
          'name': 1,
          'price': 1,
          'date': 1
        }
      }
    ]
    histories = self.history_collection.aggregate(pipeline)
    for history in histories:
      data.append({
        'id': str(history.get('_id')),
        'name': history.get('name'),
        'price': history.get('price'),
        'date': history.get('date'),
      })
    return data

class LastStocks(Stock):
  def get(self):
    data = self.get_last_stocks()
    log(data)

    response = jsonify(status="OK", data=data)
    return make_response(response, 200)

class LastStockByName(Stock):
  def get(self, name: str):
    data = self.get_last_stock_by_name(name)
    log(data)

    response = jsonify(status="OK", data=data)
    return make_response(response, 200)
