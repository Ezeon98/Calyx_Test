import logging

logger = logging.getLogger('debug.log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.addHandler(fh)

def log(log, kind):
    if kind == 'error':
        logger.error(log)
    if kind == 'info':
        logger.info(log)