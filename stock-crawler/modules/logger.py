import logging

def log(msg):
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
  logger = logging.getLogger()
  logger.debug(msg)
