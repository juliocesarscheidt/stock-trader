from stock.common.logger import log
from stock.domain.stock import Stock
from stock.adapter.mongo import Mongo
from stock.adapter.abstract_mongo import AbstractMongo
from stock.repository.abstract_repository import AbstractRepository


class StockRepository(AbstractRepository):
    mongo: AbstractMongo
    collection: None

    def __init__(self):
        self.mongo = Mongo()
        self.collection = self.mongo.database["history"]

    def find_last_stock(self, args: dict) -> dict:
        data = None
        try:
            # sort descending
            histories = self.collection.find(args).sort("date", -1).skip(0).limit(1)
            # this will receive a cursor
            for history in histories:
                data = Stock(
                    str(history.get("_id")),
                    history.get("name"),
                    history.get("country"),
                    history.get("price"),
                    history.get("date"),
                )
        except Exception as e:
            log(e)
            return None

        log(data)
        return data

    def find_last_stocks(self, country=None) -> list:
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

        try:
            # sort descending
            histories = self.collection.aggregate(pipeline)
            # this will receive a cursor
            for history in histories:
                data.append(
                    Stock(
                        str(history.get("_id")),
                        history.get("name"),
                        history.get("country"),
                        history.get("price"),
                        history.get("date"),
                    )
                )
        except Exception as e:
            log(e)
            return []

        log(data)
        return data
