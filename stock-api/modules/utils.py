import os
import pika

from datetime import datetime

def get_datetime_now_iso() -> str:
  return datetime.utcnow().isoformat()

def convert_value_to_float(value: str) -> float:
  return float(value.replace(',', '.'))

def get_rabbitmq_channel(rabbitmq_uri):
  params = pika.URLParameters(rabbitmq_uri)
  connection = pika.BlockingConnection(params)
  return connection.channel()
