import os
import sys
import pika
import urllib3
import time

from pymongo import MongoClient
from urllib.parse import urljoin, unquote_plus
from threading import Thread

from modules.mongo import MongoConnection
from modules.utils import get_http_client
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

  mongoConnection = MongoConnection(MONGO_URI)
  log(mongoConnection.history_collection)
  try:
    if mongoConnection.history_collection is None:
      mongoConnection.connect_mongo_and_get_collection()
  except Exception as e:
    log(e)

  threads = []

  # first thread, to fetch existing stocks and crawl them again, it uses mongodb connetion
  t1 = Thread(target=fetch_and_crawl, args=[http_client, mongoConnection.history_collection])
  threads.append(t1)

  # second thread, to consume from queue new stocks to crawl, it uses mongodb and rabbitmq connetion
  t2 = Thread(target=consume_and_crawl, args=[http_client, mongoConnection.history_collection])
  threads.append(t2)

  for t in threads:
    t.start()
