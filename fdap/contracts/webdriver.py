from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from typing import Union
from fdap.utils.loggeradapter import LoggerAdapter
from fdap.contracts.blog_client import BlogLoginInfo


class WebDriverHandler(ABC):
    _web_driver: WebDriver
    _logger: LoggerAdapter
    _config: dict
    _login_data: BlogLoginInfo

    def __init__(
            self,
            web_driver: WebDriver,
            logger: LoggerAdapter,
            config: dict = None,
            login_data: BlogLoginInfo = None
    ):
        self._web_driver = web_driver
        self._logger = logger
        self._config = config
        self._login_data = login_data

    def run(self, url: str) -> Union[bool, any]:
        try:
            self._web_driver.get(url)
            result = self.handle()
            self._web_driver.close()
            return result
        except WebDriverException as e:
            self._logger.error(e.msg)
            self._logger.error(e.stacktrace)
            return False

    @abstractmethod
    def handle(self):
        pass
