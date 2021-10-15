import pika
import urllib3

from pymongo import MongoClient
from datetime import datetime

def get_datetime_now_iso() -> str:
  datetime_parts = datetime.utcnow().isoformat().split('.')
  datetime_now = '%s.%sZ' % (datetime_parts[0], datetime_parts[1][0:3])
  return datetime_now

def convert_value_to_float(value: str) -> float:
  return float(value.replace(',', '.'))

def get_http_client():
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  return urllib3.PoolManager()

def get_rabbitmq_channel(rabbitmq_uri):
  params = pika.URLParameters(rabbitmq_uri)
  connection = pika.BlockingConnection(params)
  return connection.channel()

def get_mongo_client(mongo_uri):
  return MongoClient(mongo_uri)
