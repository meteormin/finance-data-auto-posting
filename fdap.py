# execute fdap
from fdap.application import Application


def run(app: Application):
    from fdap.database.database import init_db
    from fdap.app.autopost.autopost import AutoPost
    from fdap.app.tistory.tistory_client import TistoryClient

    init_db()

    tistory_login_info = app.get('tistory_login_info')
    tistory_client = app.get('tistory_client')
    if isinstance(tistory_client, TistoryClient):
        tistory_client.login(tistory_login_info)
        # print(tistory_client)

        service = app.get('auto_post')

        if isinstance(service, AutoPost):
            service.auto()
            # print(service)


if __name__ == "__main__":
    import fdap

    fdap.app.bootstrap(run)
