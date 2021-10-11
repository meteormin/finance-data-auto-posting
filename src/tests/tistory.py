from src.tests.testable import Testable


class Tistory(Testable):
    TAG: str = 'test: tistory'

    def __init__(self):
        super().__init__()

    def handle(self):
        login = self._login()
        _list = self._list(login['access_token'])

        return {
            'login': login,
            'list': _list
        }

    def _login(self):
        self.TAG += '-login'
        from definitions import CONFIG_PATH
        from src.tistory.tistoryclient import TistoryLogin, TistoryClient, LoginInfo
        from configparser import ConfigParser

        config = ConfigParser()
        config.read(CONFIG_PATH + '/tistory.ini')
        api_config = config['api']
        kakao_config = config['kakao']
        webdriver_config = config['webdriver']

        client = TistoryClient(api_config['url']).set_login(
            TistoryLogin(
                api_config['url'],
                webdriver_config
            ))

        login_info = LoginInfo(
            client_id=api_config['client_id'],
            client_secret=api_config['client_secret'],
            redirect_uri=api_config['redirect_uri'],
            response_type=api_config['response_type'],
            kakao_id=kakao_config['id'],
            kakao_password=kakao_config['password'],
            state=api_config['state']
        )

        client.login(login_info)

        return {'access_token': client.access_token}

    def _list(self, access_token: str):
        self.TAG += '-list'
        from definitions import CONFIG_PATH
        from src.tistory.tistoryclient import Apis, TistoryClient, Post
        from configparser import ConfigParser

        config = ConfigParser()
        config.read(CONFIG_PATH + '/tistory.ini')
        api_config = config['api']
        kakao_config = config['kakao']
        webdriver_config = config['webdriver']

        client = TistoryClient(api_config['url']).set_apis(
            Apis().set_post(Post(api_config['url'], access_token, api_config['blog_name']))
        )

        res = client.apis().post().list()

        return res
