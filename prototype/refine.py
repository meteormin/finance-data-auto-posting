from prototype.handler import Handler


class Refine(Handler):
    TAG: str = 'refine'

    def handle(self):
        from app.refine.refine import Refine
        from prototype.kiwoom import Kiwoom
        from prototype.opendart import Opendart
        basic_info = Kiwoom(self._save_result).handle()
        acnt = Opendart(self._save_result).handle()

        refine = Refine()

        refine_data = refine.refine_single(basic_info, acnt)

        return {
            'refined': {
                'stock_info': refine_data.basic_info.__dict__,
                'finance_data': refine_data.finance_data.__dict__
            }
        }
