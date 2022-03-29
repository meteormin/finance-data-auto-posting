# Resolve dependency injection
# use: from fdap.app.tistory import TistoryClient

def service():
    from fdap.app.tistory.tistory_client import TistoryClient, LoginInfo
    from fdap.config.config import Config

    config = Config.TISTORY
    api_config = config['api']
    kakao_config = config['kakao']

    client = TistoryClient(api_config['url'], config)
    login_info = LoginInfo(
        client_id=api_config['client_id'],
        client_secret=api_config['client_secret'],
        redirect_uri=api_config['redirect_uri'],
        response_type=api_config['response_type'],
        login_id=kakao_config['id'],
        login_password=kakao_config['password'],
        state=api_config['state']
    )

    client.login(login_info)

    return client
