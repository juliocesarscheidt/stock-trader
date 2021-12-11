import os

from pymongo import MongoClient

from .logger import log

MONGODB_TIMEOUT_SECONDS = int(os.environ.get("MONGODB_TIMEOUT_SECONDS", "5"))
MONGODB_POOL_SIZE = int(os.environ.get("MONGODB_POOL_SIZE", "10"))
MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "stocks")


class MongoConnection:
    mongo_client = None
    history_collection = None

    def __init__(self, __mongo_uri):
        self.__mongo_uri = __mongo_uri
        self.connect_mongo_and_get_collection()

    def get_mongo_client(self):
        return MongoClient(
            self.__mongo_uri,
            maxPoolSize=MONGODB_POOL_SIZE,
            socketTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
            connectTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
            serverSelectionTimeoutMS=(MONGODB_TIMEOUT_SECONDS * 1000),
        )

    def connect_mongo_and_get_collection(self):
        try:
            if self.mongo_client is None:
                self.mongo_client = self.get_mongo_client()

            self.history_collection = self.mongo_client[MONGO_DATABASE]["history"]
        except Exception as e:
            log(e)
            raise e
