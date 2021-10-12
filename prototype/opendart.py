from prototype.handler import Handler


class Opendart(Handler):
    TAG: str = 'opendart'

    def handle(self):
        from app.opendart.opendart_service import OpenDartService

        service = OpenDartService()
        corp_code = service.get_corp_code_by_stock_code('005930')
        single_data = service.get_single(corp_code.corp_code, '2021', service.Q1)
        collect = single_data['005930']

        return collect
