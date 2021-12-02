import os

from flask_restful import Resource
from flask import make_response, jsonify
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

from .mongo import MongoConnection
from .logger import log
from .publisher import publish
from .utils import get_rabbitmq_channel

MONGO_URI = os.environ.get("MONGO_URI")

RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
RABBITMQ_EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
RABBITMQ_ROUTING_KEY = os.environ.get("RABBITMQ_ROUTING_KEY")

RETRY_MAX_ATTEMPS = int(os.environ.get("RETRY_MAX_ATTEMPS", "3"))


class Stock(Resource):
    mongo_connection = None

    def __init__(self):
        self.connect_mongo_and_get_collection()

    def connect_mongo_and_get_collection(self):
        self.mongo_connection = MongoConnection(MONGO_URI)
        log(self.mongo_connection.history_collection)
        try:
            if self.mongo_connection.history_collection is None:
                self.mongo_connection.connect_mongo_and_get_collection()
        except Exception as e:
            log(e)
            raise e

    def find_last_stock(self, args: dict):
        data = None
        log(self.mongo_connection.history_collection)
        try:
            if self.mongo_connection.history_collection is None:
                self.connect_mongo_and_get_collection()
            # sort descending
            histories = (
                self.mongo_connection.history_collection.find(args)
                .sort("date", -1)
                .skip(0)
                .limit(1)
            )
            log(histories)
            # this will receive a cursor
            for history in histories:
                data = {
                    "id": str(history.get("_id")),
                    "name": history.get("name"),
                    "country": history.get("country"),
                    "price": history.get("price"),
                    "date": history.get("date"),
                }
        except Exception as e:
            log(e)
            return None
        if data is None:
            # the message needs to be published, we will retry RETRY_MAX_ATTEMPS times
            try:
                for attempt in Retrying(
                    stop=stop_after_attempt(RETRY_MAX_ATTEMPS), wait=wait_exponential()
                ):
                    with attempt:
                        if "country" in args:
                            # publish to queue, to be crawled, only if there is a country specified
                            channel = get_rabbitmq_channel(RABBITMQ_URI)
                            publish(
                                channel, args, RABBITMQ_EXCHANGE, RABBITMQ_ROUTING_KEY
                            )
                        return None

            except RetryError as e:
                log(e.last_attempt.attempt_number)
                return None
            except Exception as e:
                log(e)
                raise e

        return data

    def find_last_stocks(self, country=None):
        data = []
        # sort descending
        pipeline = [
            {"$sort": {"date": -1}},
            {
                "$group": {
                    "_id": ["$name", "$country"],
                    "object_id": {"$first": "$_id"},
                    "name": {"$first": "$name"},
                    "country": {"$first": "$country"},
                    "price": {"$first": "$price"},
                    "date": {"$first": "$date"},
                }
            },
            {
                "$project": {
                    "_id": "$object_id",
                    "name": 1,
                    "country": 1,
                    "price": 1,
                    "date": 1,
                }
            },
        ]
        if country is not None:
            match = {"$match": {"country": country}}
            pipeline.insert(0, match)

        log(self.mongo_connection.history_collection)
        try:
            if self.mongo_connection.history_collection is None:
                self.connect_mongo_and_get_collection()
            # sort descending
            histories = self.mongo_connection.history_collection.aggregate(pipeline)
            log(histories)
            # this will receive a cursor
            for history in histories:
                data.append(
                    {
                        "id": str(history.get("_id")),
                        "name": history.get("name"),
                        "country": history.get("country"),
                        "price": history.get("price"),
                        "date": history.get("date"),
                    }
                )
        except Exception as e:
            log(e)
            return []
        return data


class LastStocks(Stock):
    def get(self):
        return_code = 200
        try:
            data = self.find_last_stocks()
            response = jsonify(status="OK", data=data)
        except Exception as e:
            log(e)
            response = jsonify(
                status="Failure", data={"message": "Internal Server Error"}
            )
            return_code = 500
        return make_response(response, return_code)


class LastStocksByCountry(Stock):
    def get(self, country: str):
        return_code = 200
        try:
            data = self.find_last_stocks(country)
            response = jsonify(status="OK", data=data)
        except Exception as e:
            log(e)
            response = jsonify(
                status="Failure", data={"message": "Internal Server Error"}
            )
            return_code = 500
        return make_response(response, return_code)


class LastStockByName(Stock):
    def get(self, name: str):
        return_code = 200
        try:
            args = {"name": name}
            data = self.find_last_stock(args)
            response = jsonify(status="OK", data=data)
        except Exception as e:
            log(e)
            response = jsonify(
                status="Failure", data={"message": "Internal Server Error"}
            )
            return_code = 500
        return make_response(response, return_code)


class LastStockByCountryAndName(Stock):
    def get(self, country: str, name: str):
        return_code = 200
        try:
            args = {"country": country, "name": name}
            data = self.find_last_stock(args)
            response = jsonify(status="OK", data=data)
        except Exception as e:
            log(e)
            response = jsonify(
                status="Failure", data={"message": "Internal Server Error"}
            )
            return_code = 500
        return make_response(response, return_code)
