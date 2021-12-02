import os

from threading import Thread

from modules.mongo import MongoConnection
from modules.utils import get_http_client
from modules.logger import log
from modules.consumer import consume
from modules.processor import process

MONGO_URI = os.environ.get("MONGO_URI")

if __name__ in "__main__":
    log("[INFO] Starting Crawler...")

    http_client = get_http_client()

    mongo_connection = MongoConnection(MONGO_URI)
    log(mongo_connection.history_collection)
    try:
        if mongo_connection.history_collection is None:
            mongo_connection.connect_mongo_and_get_collection()
    except Exception as e:
        log(e)

    threads = []
    # first thread, to fetch existing stocks and crawl them again, it uses mongodb connetion
    t1 = Thread(target=process, args=[http_client, mongo_connection.history_collection])
    threads.append(t1)
    # second thread, to consume from queue new stocks to crawl, it uses mongodb and rabbitmq connetion
    t2 = Thread(target=consume, args=[http_client, mongo_connection.history_collection])
    threads.append(t2)

    for t in threads:
        t.start()
