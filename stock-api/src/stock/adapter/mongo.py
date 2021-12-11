import os

from pymongo import MongoClient

from stock.config import get_mongo_config
from stock.common.logger import log
from stock.adapter.abstract_mongo import AbstractMongo

MONGODB_TIMEOUT_SECONDS = int(os.environ.get("MONGODB_TIMEOUT_SECONDS", "10"))
MONGODB_POOL_SIZE = int(os.environ.get("MONGODB_POOL_SIZE", "10"))


class Mongo(AbstractMongo):
    config = None
    client = None
    database = None

    def __init__(self):
        self.config = get_mongo_config()
        self.set_database()

    def get_client(self):
        return MongoClient(
            self.config["uri"],
            maxPoolSize=MONGODB_POOL_SIZE,
            socketTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
            connectTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
            serverSelectionTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
        )

    def set_database(self, database=None):
        if database is None:
            database = self.config["database"]

        try:
            if self.client is None:
                self.client = self.get_client()

            self.database = self.client[database]
        except Exception as e:
            log(e)
