import selenium.common.exceptions
import time
import requests
from typing import Union, Dict
from modules.client.client import Client
from modules.utils.util import make_url
from selenium import webdriver
from dataclasses import dataclass
from definitions import CONFIG_PATH
from configparser import ConfigParser, SectionProxy
from modules.utils.customlogger import CustomLogger
from modules.contracts.blogclient import BlogClient, BlogPost


@dataclass(frozen=True)
class LoginInfo:
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    kakao_id: str
    kakao_password: str
    state: str = ''


@dataclass(frozen=True)
class AccessTokenRequest:
    client_id: str
    client_secret: str
    redirect_uri: str
    code: str
    grant_type: str = 'authorization_code'


@dataclass(frozen=False)
class PostData:
    title: str
    content: str
    published: str
    slogan: str
    tag: str
    password: str
    visibility: int = 0
    category: int = 0
    acceptComment: int = 1


class TistoryLogin(Client):

    def __init__(self, host: str, config: SectionProxy):
        super().__init__(host)
        self._config = config
        self._logger = CustomLogger.logger('automatic-posting', __name__)

    def access_token(self, req: AccessTokenRequest):
        self._logger.info('request access_token')
        method = '/oauth/access_token'
        url = make_url(self.get_host(), method, {
            'client_id': req.client_id,
            'client_secret': req.client_secret,
            'redirect_uri': req.redirect_uri,
            'code': req.code,
            'grant_type': req.grant_type
        })

        self._logger.debug(url)

        return self._set_response(requests.get(url))

    def authorize(self, login_info: LoginInfo):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        web_driver = webdriver.Chrome(self._config['driver_name'], chrome_options=options)

        url = self.get_host()
        method = '/oauth/authorize'
        url = make_url(url, method, {
            'client_id': login_info.client_id,
            'redirect_uri': login_info.redirect_uri,
            'response_type': login_info.response_type,
            'state': login_info.state
        })

        web_driver.get(url=url)
        try:
            element = web_driver.find_element_by_css_selector(self._config['confirm_btn'])
            element.click()
            url = web_driver.current_url
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.stacktrace)

        try:
            web_driver.find_element_by_css_selector(self._config['kakao_login_link'])
            self._logger.info('redirect kakao login: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail redirect kakao login: ' + web_driver.current_url)

        try:
            web_driver.get(web_driver.current_url)
            self._logger.info('request: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.stacktrace)

        self._logger.info('sleep 3s')
        time.sleep(3)

        web_driver.find_element_by_css_selector(self._config['kakao_email_input']).send_keys(login_info.kakao_id)
        self._logger.info('input email')

        web_driver.find_element_by_css_selector(self._config['kakao_pass_input']).send_keys(login_info.kakao_password)
        self._logger.info('input password')

        web_driver.find_element_by_css_selector(self._config['kakao_login_submit']).click()
        self._logger.info('submit login form')
        self._logger.info('sleep 3s')
        time.sleep(3)

        try:
            web_driver.find_element_by_css_selector('confirm_btn').click()
            self._logger.info('success login: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail login: ' + web_driver.current_url)

        url = web_driver.current_url
        web_driver.close()
        self._logger.info('close webdriver')

        return self._set_response(requests.get(url))


class Post(Client, BlogPost):

    def __init__(self, host: str, token: str, blog_name: str):
        super().__init__(host=host)
        self.access_token = token
        self.blog_name = blog_name

    def list(self, page: int = 1):
        method = '/list'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json',
            'page': page
        })

        self._set_response(requests.get(url))

    def read(self, post_id: int):
        method = '/read'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'postId': post_id
        })
        return self._set_response(requests.get(url))

    def write(self, post: PostData):
        method = '/write'
        post_data = post.__dict__
        post_data.update({
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json'
        })

        url = make_url(self.get_host(), method, post_data)

        return self._set_response(requests.post(url))

    def modify(self, obj: object):
        pass

    def attach(self, filename: str, contents: str):
        method = '/attach'
        files = {filename: contents}
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name
        })
        return self._set_response(requests.post(url, files=files))


class Apis(Client):

    def __init__(self, host: str, token: str, blog_name: str):
        super().__init__(host=host)
        self.access_token = token
        self.blog_name = blog_name

    def post(self) -> BlogPost:
        return Post(self.get_host(), self.access_token, self.blog_name)


class TistoryClient(Client, BlogClient):
    blog_name: str = None
    access_token: str = None

    def __init__(self, host: str):
        super().__init__(host=host)
        self._config = ConfigParser()
        self._config.read(CONFIG_PATH + '/tistory.ini')
        self._logger = CustomLogger.logger('automatic-posting', __name__)
        self.blog_name = self._config['api']['blog_name']

    def login(self, login_info: LoginInfo) -> Union[Dict[str, str], None]:
        login = TistoryLogin(self.get_host(), self._config['webdriver'])
        res = login.authorize(login_info)

        if 'code' in res:
            self._logger.info('code: ' + res['code'])
            req = AccessTokenRequest(
                client_id=login_info.client_id,
                client_secret=login_info.client_secret,
                redirect_uri=login_info.redirect_uri,
                code=res['code']
            )
            token = login.access_token(req)
        else:
            self._logger.warning('fail issue token')
            return None

        [name, token] = token.split('=')
        self._logger.debug(name + ': ' + token)

        self.access_token = token

        return {name: token}

    def apis(self) -> Union[Apis, None]:
        if self.access_token is None:
            return None
        return Apis(self.get_host(), self.access_token, self.blog_name)
