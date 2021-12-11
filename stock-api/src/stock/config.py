import os


def get_mongo_config():
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DATABASE = os.environ.get("MONGO_DATABASE")
    return {
        "uri": MONGO_URI,
        "database": MONGO_DATABASE,
    }


def get_rabbitmq_config():
    RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
    RABBITMQ_EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
    RABBITMQ_ROUTING_KEY = os.environ.get("RABBITMQ_ROUTING_KEY")
    return {
        "uri": RABBITMQ_URI,
        "exchange": RABBITMQ_EXCHANGE,
        "routing_key": RABBITMQ_ROUTING_KEY,
    }


def get_xray_config():
    AWS_XRAY_DAEMON_ADDRESS = os.environ.get("AWS_XRAY_DAEMON_ADDRESS")
    return {
        "address": AWS_XRAY_DAEMON_ADDRESS,
    }
