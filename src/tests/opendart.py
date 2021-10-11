from src.tests.testable import Testable
from src.opendart.opendart_data import AcntCollection


class Opendart(Testable):
    TAG: str = 'test-opendart'

    def handle(self):
        from src.opendart.opendart_service import OpenDartService

        service = OpenDartService()
        corp_code = service.get_corp_code_by_stock_code('005930')
        single_data = service.get_single(corp_code.corp_code, '2021', service.Q1.value)
        collect = AcntCollection(single_data['005930'])

        return collect.to_json()
