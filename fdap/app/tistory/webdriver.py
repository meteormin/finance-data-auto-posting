from fdap.contracts.blog_client import BlogLoginInfo
from fdap.contracts.webdriver import WebDriverHandler as Handler
from fdap.utils.loggeradapter import LoggerAdapter
from fdap.utils.util import get_query_str_dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from dataclasses import dataclass
import time
import selenium.common.exceptions


@dataclass()
class CustomElement:
    by: str
    value: str
    action: str
    func: str = 'find_element'


class WebDriverController:
    _history: list
    _web_driver: WebDriver

    def __init__(self, driver: WebDriver):
        self._web_driver = driver

    def add_element(self, element: CustomElement):
        class_method = getattr(WebDriver, element.func)
        obj = class_method(self._web_driver, element.by, element.value)
        if isinstance(obj, WebElement):
            obj_method = getattr(obj, element.action)
            self._history.append(obj_method(obj))
        return self

    def add(self, func_name, **kwargs):
        class_method = getattr(WebDriver, func_name)
        self._history.append(class_method(self._web_driver, **kwargs))
        return self

    def get_history(self):
        return self._history


class CustomHandler(Handler):
    TYPES = [
        'element',
        'function'
    ]

    FUNCS = [
        'find_element',
        'get'
    ]

    _dynamic: list = [
        {
            'type': 'element',
            'name': 'find_element',
            'by': 'css selector',
            'value': '.confirm',
            'action': 'click'
        },
        {
            'type': 'function',
            'name': 'get',
            'args': {
                'url': 'url'
            }
        }
    ]

    def __init__(
            self,
            web_driver: WebDriver,
            logger: LoggerAdapter,
            config_list: list = None,
    ):
        super().__init__(web_driver, logger)
        self._dynamic = config_list

    def handle(self):
        controller = WebDriverController(self._web_driver)
        for item in self._dynamic:
            if item['name'] not in self.FUNCS:
                self._logger.warning(f"{item['name']} is not support function")
                continue

            if item['type'] not in self.TYPES:
                self._logger.warning(f"{item['type']} is not support type")
                continue
            elif item['type'] == 'element':
                controller.add_element(
                    CustomElement(
                        by=item['by'],
                        value=item['value'],
                        action=item['action'],
                        func=item['name']
                    )
                )
            else:
                controller.add(func_name=item['name'], **item['args'])

        return controller.get_history()


class WebDriverHandler(Handler):
    _web_driver: WebDriver
    _logger: LoggerAdapter
    _config: dict
    _login_data: BlogLoginInfo

    def handle(self):
        try:
            element = self._web_driver.find_element(By.CSS_SELECTOR, self._config['confirm_btn'])
            element.click()
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('No Such Element 1: confirm_btn')
            self._logger.warning(e.msg)

        try:
            self._web_driver.find_element(By.CSS_SELECTOR, self._config['kakao_login_link']).click()
            self._logger.info('redirect kakao login: ' + self._web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail redirect kakao login: ' + self._web_driver.current_url)
            self._logger.warning(e.msg)
        try:
            self._web_driver.get(self._web_driver.current_url)
            self._logger.info('request: ' + self._web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.stacktrace)

        self._logger.info('sleep 3s')
        time.sleep(3)
        try:
            self._web_driver.find_element(By.CSS_SELECTOR, self._config['kakao_email_input']) \
                .send_keys(self._login_data.login_id)
            self._logger.info('input email')

            time.sleep(1)

            self._web_driver.find_element(By.CSS_SELECTOR, self._config['kakao_pass_input']) \
                .send_keys(self._login_data.login_password)
            self._logger.info('input password')

            self._web_driver.find_element(By.CSS_SELECTOR, self._config['kakao_login_submit']).click()
            self._logger.info('submit login form')

            self._logger.info('sleep 3s')
            time.sleep(3)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.msg)

        try:
            self._web_driver.find_element(By.CSS_SELECTOR, self._config['confirm_btn']).click()
            self._logger.info('success login: ' + self._web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail login: ' + self._web_driver.current_url)

        url = self._web_driver.current_url

        self._logger.info('close webdriver')

        return get_query_str_dict(url)
