import logging


def log(msg):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )
    logger = logging.getLogger()
    logger.info(msg)
