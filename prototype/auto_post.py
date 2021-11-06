from prototype.handler import Handler
from fdap.app.autopost.parameters import Parameters
from fdap.app.autopost.autopost import AutoPost as Module
from fdap.app.kiwoom.kiwoom_service import KiwoomService
from fdap.app.opendart.opendart_service import OpenDartService
from fdap.app.tistory.tistory_client import TistoryClient
from fdap.app.refine.refine import Refine
from fdap.app.repositories.post_repository import PostsRepository
from fdap.utils.util import config_json
from fdap.config.config import Config
from fdap.database.database import db_session, init_db


class AutoPost(Handler):
    TAG: str = 'auto-post'

    @staticmethod
    def make_module():
        init_db()

        kiwoom_config = config_json(Config.KOAPY)
        tistory_config = config_json(Config.TISTORY)
        opendart_config = config_json(Config.OPENDART)

        return Module(
            kiwoom=KiwoomService(
                _id=kiwoom_config['account']['id'],
                password=kiwoom_config['account']['password']
            ),
            opendart=OpenDartService(
                url=opendart_config['api']['url'],
                api_key=opendart_config['api']['api_key']
            ),
            refine=Refine(),
            tistory=TistoryClient(
                host=tistory_config['api']['url'],
                config=tistory_config
            ),
            repo=PostsRepository(db_session=db_session)
        )

    def handle(self):
        module = self.make_module()

        parameters = Parameters(
            sector_name='건설업',
            sector_code='018',
            year='2021',
            quarter=1
        )

        result = module.run(parameters)

        # kiwoom api 연결 종료
        module.kiwoom.disconnect()
        return result
