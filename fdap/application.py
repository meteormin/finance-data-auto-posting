from dependency_injector import containers
from fdap.config.config import Config
from fdap.utils.customlogger import CustomLogger
from fdap.utils.loggeradapter import LoggerAdapter
from typing import Callable


class Application:
    _container: containers.DeclarativeContainer
    _logger: LoggerAdapter

    def __init__(self, container: containers.DeclarativeContainer, callback: Callable = None):
        self._logger = CustomLogger.logger('root', 'application')
        self._container = container
        self._container.config.from_dict(Config.all())
        self._container.init_resources()
        if callback is not None:
            self.bootstrap(callback)

    def get(self, name: str) -> any:
        return self._container.providers.get(name)()

    def bootstrap(self, callback: Callable):
        try:
            callback(self)
        except Exception as e:
            self._logger.error('Failed Bootstrapping...')
            self._logger.error(e)
