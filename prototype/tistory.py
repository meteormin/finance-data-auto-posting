from prototype.handler import Handler
from fdap.app.tistory.tistory_client import TistoryLogin, TistoryClient, LoginInfo
from fdap.utils.util import config_json


class Tistory(Handler):
    TAG: str = 'tistory'
    client: TistoryClient

    def handle(self):
        login = self.login()
        _list = self.list(login['access_token'])

        return {
            'login': login,
            'list': _list
        }

    def login(self):
        self.TAG += '-login'

        config = config_json('tistory')
        api_config = config['api']
        kakao_config = config['kakao']

        self.client = TistoryClient(api_config['url'], config)

        login_info = LoginInfo(
            client_id=api_config['client_id'],
            client_secret=api_config['client_secret'],
            redirect_uri=api_config['redirect_uri'],
            response_type=api_config['response_type'],
            kakao_id=kakao_config['id'],
            kakao_password=kakao_config['password'],
            state=api_config['state']
        )

        self.client.login(login_info)

        return {'access_token': self.client.access_token}

    def list(self, access_token: str):
        self.TAG += '-list'
        from fdap.app.tistory.tistory_client import TistoryClient
        from fdap.utils.util import config_json

        config = config_json('tistory')
        api_config = config['api']

        client = TistoryClient(api_config['url'], config)
        post = client.apis().post()
        post.access_token = access_token
        res = post.list()

        return res
