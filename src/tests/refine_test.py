from src.tests.testable import Testable


class RefineTest(Testable):
    TAG: str = 'refine-test'

    def handle(self):
        from src.refine import Refine
        from src.tests.koapy import Koapy
        from src.tests.opendart import Opendart
        basic_info = Koapy(self._save_result).handle()
        acnt = Opendart(self._save_result).handle()

        refine = Refine()

        refine_data = refine.refine_single(basic_info, acnt)

        return {
            'refined': {
                'stock_info': refine_data.basic_info.__dict__,
                'finance_data': refine_data.finance_data.__dict__
            }
        }
