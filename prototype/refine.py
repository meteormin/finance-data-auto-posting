from prototype.handler import Handler


class Refine(Handler):
    TAG: str = 'refine'

    def handle(self):
        from fdap.app.refine.refine import Refine
        from prototype.kiwoom import Kiwoom
        from prototype.opendart import Opendart
        basic_info = Kiwoom(self._save_result).handle()
        acnt = Opendart(self._save_result).handle()

        refine = Refine()

        refine_data = refine.refine_single(basic_info, acnt)

        return refine_data
        # return refine_data.to_dict()
