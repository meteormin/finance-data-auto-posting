from fdap.prototype.handler import Handler
from fdap.app.autopost import instance


class AutoPost(Handler):
    TAG: str = 'auto-post'

    @staticmethod
    def make_module():
        return instance()

    def handle(self):
        module = self.make_module()
        # result = module.run(
        #     Parameters(
        #         sector_code='20',
        #         sector_name='통신업',
        #         year='2021',
        #         quarter=3
        #     )
        # )
        result = module.auto()
        # kiwoom api 연결 종료를 위해...
        module.close()

        return result
