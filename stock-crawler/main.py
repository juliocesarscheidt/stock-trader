import os
import sys
import pika
import urllib3
import time

from pymongo import MongoClient
from urllib.parse import urljoin, unquote_plus
from threading import Thread

from modules.crawler import crawl_stock_price
from modules.utils import get_http_client, get_mongo_client
from modules.logger import log
from modules.consumer import consume
from modules.processor import process

MONGO_URI = os.environ.get('MONGO_URI')

def consume_and_crawl(__http_client, __history_collection):
  consume(__http_client, __history_collection)

def fetch_and_crawl(__http_client, __history_collection):
  process(__http_client, __history_collection)

if __name__ in '__main__':
  log('[INFO] Starting Crawler...')

  http_client = get_http_client()

  mongo_client = get_mongo_client(MONGO_URI)
  stocks_database = mongo_client['stocks']
  history_collection = stocks_database['history']

  threads = []

  # first thread, to fetch existing stocks and crawl them again
  t1 = Thread(target=fetch_and_crawl, args=[http_client, history_collection])
  threads.append(t1)

  # second thread, to consume from queue new stocks to crawl
  t2 = Thread(target=consume_and_crawl, args=[http_client, history_collection])
  threads.append(t2)

  for t in threads:
    t.start()
