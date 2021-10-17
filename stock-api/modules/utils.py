import os
import pika

from datetime import datetime

def get_datetime_now_iso() -> str:
  datetime_parts = datetime.utcnow().isoformat().split('.')
  datetime_now = '%s.%sZ' % (datetime_parts[0], datetime_parts[1][0:3])
  return datetime_now

def convert_value_to_float(value: str) -> float:
  return float(value.replace(',', '.'))

def get_rabbitmq_channel(rabbitmq_uri):
  params = pika.URLParameters(rabbitmq_uri)
  connection = pika.BlockingConnection(params)
  return connection.channel()
