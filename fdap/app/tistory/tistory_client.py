import requests
from typing import Union
from fdap.utils.util import make_url
from selenium import webdriver
from fdap.definitions import ROOT_DIR
from fdap.utils.customlogger import CustomLogger
from fdap.app.tistory.tistory_data import *
from fdap.app.tistory.webdriver import WebDriverHandler
from fdap.contracts.blog_client import *


class TistoryLogin(BlogLogin):
    _end_point = '/oauth'

    def __init__(self, host, config: dict):
        super().__init__(host=host, config=config['webdriver'])
        self._logger = CustomLogger.logger('automatic-posting', __name__)

    def login(self, login_info: LoginInfo) -> Union[None, dict]:
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
        self.access_token = token
        return {name: self.access_token}

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

        return self._set_response(requests.get(url, verify=False))

    def _authorize(self, login_info: LoginInfo):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')

        web_driver = webdriver.Chrome(executable_path=ROOT_DIR + '\\' + self._config['driver_name'],
                                      chrome_options=options)

        handler = WebDriverHandler(
            web_driver,
            self._logger,
            self._config,
            login_info
        )

        url = self.get_host()
        method = self._end_point + '/authorize'
        url = make_url(url, method, {
            'client_id': login_info.client_id,
            'redirect_uri': login_info.redirect_uri,
            'response_type': login_info.response_type,
            'state': login_info.state
        })

        return handler.run(url)


class Post(BlogPost):
    blog_name: str
    _resource: str = '/post'
    _user_agent: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }

    def __init__(self, host: str, config: Dict[str, any]):
        super().__init__(host=host, config=config['api'])
        self.blog_name = self._config['blog_name']
        if self._config['user_agent'] is not None:
            self._user_agent = {'User-Agent': self._config['user_agent']}

        self._logger = CustomLogger.logger('automatic-posting', __name__)

    def list(self, page: int = 1):
        method = self._resource + '/list'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json',
            'page': page
        })

        self._logger.debug(url)
        return self._set_response(requests.get(url, verify=False))

    def read(self, post_id: int):
        method = self._resource + '/read'
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'postId': post_id
        })
        return self._set_response(requests.get(url, verify=False))

    def write(self, post: BlogPostData):
        method = self._resource + '/write'
        post_data = post.__dict__
        post_data.update({
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json'
        })

        url = make_url(self.get_host(), method)

        return self._set_response(requests.post(url, data=post_data, headers=self._user_agent, verify=False))

    def modify(self, obj: BlogPostData):
        pass

    def attach(self, filename: str, contents: bytes):
        method = self._resource + '/attach'
        files = {'uploadedfile': contents}
        url = make_url(self.get_host(), method, {
            'access_token': self.access_token,
            'blogName': self.blog_name,
            'output': 'json'
        })

        return self._set_response(requests.post(url, files=files, headers=self._user_agent, verify=False))


class Apis(BlogEndPoint):
    blog_name: str
    _end_point = '/apis'
    _classes = {
        'post': Post
    }

    def __init__(self, host, config: Dict[str, any]):
        super().__init__(host, config)
        for name, cls in self._classes.items():
            res = cls(host + self._end_point, config)
            self.set_resource(res.__class__, res)

    def set_post(self, post_api: Post):
        self.set_resource(post_api.__class__, post_api)
        return self

    def post(self) -> Post:
        return self.get_resource(self._classes['post'])


class TistoryClient(BlogClient):
    _config: dict

    # 의존성 바인딩
    # 정의된 클래스가 아니면 가져올 수 없다.
    # 해당 프로퍼티를 수정하여 다형성을 만족시킬 수 있다.
    _classes: Dict[str, type] = {
        'login': TistoryLogin,
        'apis': Apis
    }

    access_token: str = None

    def __init__(self, host: str, config: Dict[str, any]):
        super().__init__(host=host, config=config)
        self._config = config
        self._logger = CustomLogger.logger('automatic-posting', __name__)
        for name, cls in self._classes.items():
            end_point = cls(host, config)
            self.set_end_point(end_point.__class__, end_point)

    def set_login(self, login: TistoryLogin):
        return self.set_end_point(login.__class__, login)

    def login(self, login_info: LoginInfo) -> Union[Dict[str, str], None]:
        login = self.get_end_point(self._classes['login'])
        if isinstance(login, BlogLogin):
            login.login(login_info)
            self.set_access_token(login.access_token)
            return {'access_token': self.access_token}
        return None

    def set_apis(self, apis: Apis):
        return self.set_end_point(apis.__class__, apis)

    def apis(self) -> Apis:
        return self.get_end_point(self._classes['apis'])
