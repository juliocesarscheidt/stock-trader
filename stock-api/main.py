import os
import sys
import pika

from pymongo import MongoClient
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from modules.stocks import LastStocks, LastStockByName
from modules.health import Health
from modules.utils import convert_value_to_float, get_datetime_now_iso
from modules.logger import log

# application setup
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

if __name__ in '__main__':
  log('[INFO] Starting API...')
  # add endpoints
  api.add_resource(Health, '/api/v1/health')
  api.add_resource(LastStocks, '/api/v1/stocks/last')
  api.add_resource(LastStockByName, '/api/v1/stocks/last/<string:name>')
  # start API
  app.run(host='0.0.0.0', port='5050', debug=True)
