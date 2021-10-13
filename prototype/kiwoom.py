from prototype.handler import Handler


class Kiwoom(Handler):
    TAG: str = 'kiwoom-sectors'

    def handle(self):
        from fdap.app.kiwoom.kiwoom_service import KiwoomService

        service = KiwoomService()
        return service.get_stock('005930')
        # return service.get_sector_list()
