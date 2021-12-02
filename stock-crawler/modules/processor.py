import os
import time

from .crawler import crawl_stock_price
from .utils import get_datetime_now_iso
from .stocks import get_stocks
from .logger import log

PROCESS_INTERVAL_SECONDS = int(os.environ.get("PROCESS_INTERVAL_SECONDS", "60"))


def process(__http_client, __history_collection):
    while True:
        stocks = get_stocks(__history_collection)
        log(stocks)

        for stock in stocks:
            stock_name = stock["name"]
            stock_country = stock["country"]
            stock_price = crawl_stock_price(__http_client, stock_country, stock_name)
            log("stock_price " + str(stock_price))

            if stock_price is not None:
                stock_history = {
                    "name": stock_name,
                    "country": stock_country,
                    "price": stock_price,
                    "date": get_datetime_now_iso(),
                }
                log(stock_history)
                try:
                    __history_collection.insert_one(stock_history)
                except Exception as e:
                    log(e)
                    continue

        # sleep 60 secs
        time.sleep(PROCESS_INTERVAL_SECONDS)
