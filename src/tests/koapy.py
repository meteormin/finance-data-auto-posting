from src.tests.testable import Testable


class Koapy(Testable):
    TAG: str = 'test-koapy'

    def handle(self):
        from src.koapy.koapyservice import KoapyService

        service = KoapyService()
        return service.get_stock('005930')
