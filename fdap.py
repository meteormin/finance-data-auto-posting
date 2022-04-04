# execute fdap
from fdap.application import Application


def run(app: Application):
    from fdap.database.database import init_db
    init_db()

    service = app.get('auto_post')

    if isinstance(service, AutoPost):
        service.auto()


if __name__ == "__main__":
    import fdap
    from fdap.app.autopost.autopost import AutoPost

    fdap.app.bootstrap(run)
