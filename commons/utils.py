import logging
from auth.settings import CUSTOM_LOG


def get_logger():
    logger = logging.getLogger(name=CUSTOM_LOG)
    return logger
