import os
import sys
import pika

from pymongo import MongoClient
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from modules.stocks import LastStocks, LastStockByName
from modules.utils import convert_value_to_float, get_datetime_now_iso, get_mongo_client
from modules.logger import log

# application setup
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

MONGO_URI = os.environ.get('MONGO_URI')

if __name__ in '__main__':
  log('[INFO] Starting API...')

  mongo_client = get_mongo_client(MONGO_URI)
  stocks_database = mongo_client['stocks']
  history_collection = stocks_database['history']

  api.add_resource(LastStocks, '/v1/stocks/last', resource_class_kwargs={'history_collection': history_collection})
  api.add_resource(LastStockByName, '/v1/stocks/last/<string:name>', resource_class_kwargs={'history_collection': history_collection})

  app.run(host='0.0.0.0', port='5050', debug=True)
