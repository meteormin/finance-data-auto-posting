from src.tests.testable import Testable


class Koapy(Testable):
    TAG: str = 'test-koapy'

    def handle(self):
        from src.koapy.koapyservice import KoapyService

        service = KoapyService()
        stock_info = service.get_stock('005930')
        return {
            'single_stock': {
                '종목코드': stock_info.code,
                '종목명': stock_info.name,
                '시가총액': stock_info.capital,
                '현재가': stock_info.current_price
            }
        }
