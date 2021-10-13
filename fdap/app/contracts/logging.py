from abc import ABC
from fdap.app.utils.loggeradapter import LoggerAdapter
from fdap.app.utils.customlogger import CustomLogger


class Logging(ABC):
    _logger: LoggerAdapter
    _TAG: str = None
    _LOGGER_NAME: str = 'automatic-posting'

    def __init__(self):
        self._logger = CustomLogger.logger(
            self._LOGGER_NAME,
            self._TAG if self._TAG is not None else self.__class__.__name__
        )
