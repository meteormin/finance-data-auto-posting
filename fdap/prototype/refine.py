from fdap.prototype.handler import Handler
from fdap.app.opendart.report_code import ReportCode
from fdap.app.opendart.opendart_data import AcntCollection


class Refine(Handler):
    TAG: str = 'refine'

    def handle(self):
        from fdap.app.refine.refine import Refine
        from fdap.prototype.kiwoom import Kiwoom
        from fdap.prototype.opendart import Opendart

        params = self.get_parameters()
        sector = None
        year = '2021'
        report_code = ReportCode.Q1
        stock_code = '005930'

        if 'sector' in params:
            sector = params['sector']
            stock_code = None

        if 'year' in params:
            year = params['year']
        if 'report_code' in params:
            report_code = params['report_code']

        basic_info = Kiwoom(save_result=self._save_result, parameters={
            'sector': sector,
            'stock_code': stock_code
        }).handle()

        acnt = Opendart(save_result=self._save_result, parameters={
            'stock_info': basic_info,
            'year': year,
            'report_code': report_code
        }).handle()

        refine = Refine()

        if isinstance(acnt, AcntCollection):
            refine_data = refine.refine_single(basic_info, acnt)
        else:
            refine_data = refine.refine_multiple(basic_info, acnt)

        return refine_data
        # return refine_data.to_dict()
