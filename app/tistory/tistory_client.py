import selenium.common.exceptions
import time
import requests
from typing import Union
from app.utils.util import make_url, get_query_str_dict, config_ini
from selenium import webdriver
from definitions import ROOT_DIR
from configparser import SectionProxy
from app.utils.customlogger import CustomLogger
from app.contracts.blog_client import *
from app.tistory.tistory_data import *


class TistoryLogin(BlogEndPoint, BlogLogin):
    _end_point = '/oauth'

    def __init__(self, host: str, config: SectionProxy):
        super().__init__(host)
        self._config = config
        self._logger = CustomLogger.logger('automatic-posting', __name__)

    def login(self, login_info: LoginInfo):
        res = self._authorize(login_info)

        if 'code' in res:
            self._logger.info('code: ' + res['code'])
            req = AccessTokenRequest(
                client_id=login_info.client_id,
                client_secret=login_info.client_secret,
                redirect_uri=login_info.redirect_uri,
                code=res['code']
            )
            token = self._access_token(req)
        else:
            self._logger.warning('fail issue token')
            return None

        [name, token] = token.split('=')
        self._logger.debug(name + ': ' + token)

        return {name: token}

    def _access_token(self, req: AccessTokenRequest):
        self._logger.info('request access_token')
        method = self._end_point + '/access_token'
        url = make_url(self.get_host(), method, {
            'client_id': req.client_id,
            'client_secret': req.client_secret,
            'redirect_uri': req.redirect_uri,
            'code': req.code,
            'grant_type': req.grant_type
        })

        self._logger.debug(url)

        return self._set_response(requests.get(url))

    def _authorize(self, login_info: LoginInfo):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')

        web_driver = webdriver.Chrome(executable_path=ROOT_DIR + '\\' + self._config['driver_name'],
                                      chrome_options=options)

        url = self.get_host()
        method = self._end_point + '/authorize'
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
            self._logger.warning('No Such Element 1: confirm_btn')
            self._logger.warning(e.msg)

        try:
            web_driver.find_element_by_css_selector(self._config['kakao_login_link']).click()
            self._logger.info('redirect kakao login: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail redirect kakao login: ' + web_driver.current_url)
            self._logger.warning(e.msg)
        try:
            web_driver.get(web_driver.current_url)
            self._logger.info('request: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.stacktrace)

        self._logger.info('sleep 3s')
        time.sleep(3)
        try:
            web_driver.find_element_by_css_selector(self._config['kakao_email_input']) \
                .send_keys(login_info.kakao_id)
            self._logger.info('input email')

            time.sleep(1)

            web_driver.find_element_by_css_selector(self._config['kakao_pass_input']) \
                .send_keys(login_info.kakao_password)
            self._logger.info('input password')

            web_driver.find_element_by_css_selector(self._config['kakao_login_submit']).click()
            self._logger.info('submit login form')
            self._logger.info('sleep 3s')
            time.sleep(3)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning(e.msg)

        try:
            web_driver.find_element_by_css_selector(self._config['confirm_btn']).click()
            self._logger.info('success login: ' + web_driver.current_url)
        except selenium.common.exceptions.NoSuchElementException as e:
            self._logger.warning('fail login: ' + web_driver.current_url)

        url = web_driver.current_url
        web_driver.close()
        self._logger.info('close webdriver')

        return get_query_str_dict(url)


class Post(BlogPost):
    _resource: str = '/post'

    def __init__(self, host: str, token: str, blog_name: str):
        super().__init__(host=host)
        self.access_token = token
        self.blog_name = blog_name
        self._logger = CustomLogger.logger('automatic-posting', 'Post')

    def list(self, page: int = 1):
        method = self._resource + '/list'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json',
            'page': page
        })

        self._logger.debug(url)
        return self._set_response(requests.get(url))

    def read(self, post_id: int):
        method = self._resource + '/read'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'postId': post_id
        })
        return self._set_response(requests.get(url))

    def write(self, post: BlogPostData):
        method = self._resource + '/write'
        post_data = post.__dict__
        post_data.update({
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json'
        })

        url = make_url(self.get_host(), method, post_data)

        return self._set_response(requests.post(url))

    def modify(self, obj: BlogPostData):
        pass

    def attach(self, filename: str, contents: str):
        method = self._resource + '/attach'
        files = {filename: contents}
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name
        })
        return self._set_response(requests.post(url, files=files))


class Apis(BlogEndPoint):
    _end_point = '/apis'
    _classes = {
        'post': Post
    }

    def set_post(self, post_api: Post):
        self.set_resource(post_api.__class__, post_api)
        return self

    def post(self) -> Post:
        return self.get_resource(self._classes['post'])


class TistoryClient(BlogClient):
    blog_name: str = None
    access_token: str = None

    # 의존성 바인딩
    # 정의된 클래스가 아니면 가져올 수 없다.
    # 해당 프로퍼티를 수정하여 다형성을 만족시킬 수 있다.
    _classes: Dict[str, type] = {
        'login': TistoryLogin,
        'apis': Apis
    }

    def __init__(self, host: str):
        super().__init__(host=host)
        self._config = config_ini('tistory')
        self._logger = CustomLogger.logger('automatic-posting', __name__)
        self.blog_name = self._config['api']['blog_name']

    def set_login(self, login: TistoryLogin):
        return self.set_end_point(login.__class__, login)

    def login(self, login_info: LoginInfo) -> Union[Dict[str, str], None]:
        login = self.get_end_point(self._classes['login'])
        if isinstance(login, BlogLogin):
            token = login.login(login_info)
            if 'access_token' in token:
                self.access_token = token['access_token']
                return token
        return None

    def set_apis(self, apis: Apis):
        return self.set_end_point(apis.__class__, apis)

    def apis(self) -> Apis:
        return self.get_end_point(self._classes['apis'])
