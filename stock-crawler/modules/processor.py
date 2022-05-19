import os
import math
import schedule

from datetime import datetime

from .crawler import crawl_stock_price
from .utils import get_datetime_now_iso
from .stocks import get_stocks, count_stocks
from .logger import log

PROCESS_INTERVAL_SECONDS = int(os.environ.get("PROCESS_INTERVAL_SECONDS", "60"))


def job(__http_client, __history_collection):
    log("[INFO] Job running at " + str(datetime.now()))

    stock_histories = []
    rows_count = 0
    batch_size = 1000

    stocks_counter = count_stocks(__history_collection)
    log("stocks_counter " + str(stocks_counter))

    recursive_counter = math.ceil(stocks_counter / batch_size)
    for i in range(0, recursive_counter):
        stocks = get_stocks(__history_collection, (i * batch_size), batch_size)

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
                stock_histories.append(stock_history)
                rows_count = rows_count + 1

                if rows_count >= batch_size:
                    log("Inserting " + str(rows_count) + " rows")
                    try:
                        __history_collection.insert_many(stock_histories)
                        stock_histories = []
                        rows_count = 0
                    except Exception as e:
                        log(e)

        if rows_count >= 0:
            log("Inserting " + str(rows_count) + " rows")
            try:
                __history_collection.insert_many(stock_histories)
                stock_histories = []
                rows_count = 0
            except Exception as e:
                log(e)


def process(__http_client, __history_collection):
    log(
        "[INFO] Scheduling job to run every "
        + str(PROCESS_INTERVAL_SECONDS)
        + " seconds"
    )
    schedule.every(PROCESS_INTERVAL_SECONDS).seconds.do(
        job, __http_client=__http_client, __history_collection=__history_collection
    )
    while True:
        schedule.run_pending()
