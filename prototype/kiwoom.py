from prototype.handler import Handler


class Kiwoom(Handler):
    TAG: str = 'kiwoom'

    def handle(self):
        from app.kiwoom.kiwoom_service import KiwoomService

        service = KiwoomService()
        return service.get_stock('005930')
