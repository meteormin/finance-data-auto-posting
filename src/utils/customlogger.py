import json
import logging
import logging.config
from src.utils.loggeradapter import LoggerAdapter
from definitions import CONFIG_PATH


class CustomLogger:

    @staticmethod
    def logger(logger_name: str = 'root', tag='') -> LoggerAdapter:
        logging.config.fileConfig(CONFIG_PATH + '\\logger.ini')
        logger = logging.getLogger(logger_name)
        logger = LoggerAdapter(tag, logger)
        return logger
