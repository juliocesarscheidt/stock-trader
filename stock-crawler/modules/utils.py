import os
import pika
import json
import urllib3

from datetime import datetime


def get_datetime_now_iso() -> str:
    return datetime.utcnow().isoformat()


def convert_value_to_float(value: str) -> float:
    return float(str(value).replace(",", "."))


def get_http_client():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return urllib3.PoolManager()


def get_rabbitmq_channel(rabbitmq_uri):
    params = pika.URLParameters(rabbitmq_uri)
    connection = pika.BlockingConnection(params)
    return connection.channel()


def get_dolar_price(http_client) -> float:
    code = "USD-BRL"
    api_uri = "https://economia.awesomeapi.com.br/all"
    response = http_client.request("GET", f"{api_uri}/{code}")
    if not (response.status >= 200 and response.status < 300):
        return None
    data = json.loads(response.data)
    return convert_value_to_float(data["USD"]["ask"])
