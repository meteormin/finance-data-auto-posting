import json
import logging
import logging.config
import os

from src.utils.loggeradapter import LoggerAdapter
from definitions import CONFIG_PATH, LOG_PATH
from os.path import exists


class CustomLogger:

    @staticmethod
    def logger(logger_name: str = 'root', tag='') -> LoggerAdapter:
        if not exists(LOG_PATH):
            os.mkdir(LOG_PATH)
        if not exists(LOG_PATH + '/tests'):
            os.mkdir(LOG_PATH + '/tests')

        logging.config.fileConfig(CONFIG_PATH + '\\logger.ini')
        logger = logging.getLogger(logger_name)
        logger = LoggerAdapter(tag, logger)
        return logger
