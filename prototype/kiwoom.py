from prototype.handler import Handler


class Kiwoom(Handler):
    TAG: str = 'kiwoom-sectors'

    def handle(self):
        from fdap.app.kiwoom.kiwoom_service import KiwoomService
        params = self.get_parameters()
        stock_code = None
        sector = None
        if not params:
            stock_code = '005930'
        else:
            if 'sector' in params:
                sector = params['sector']
            elif 'stock_code' in params:
                stock_code = params['stock_code']
            else:
                stock_code = '005930'

        service = KiwoomService()
        if stock_code:
            return service.get_stock(stock_code)

        return service.get_stock_list_by_sector(sector)
