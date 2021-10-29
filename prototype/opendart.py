from prototype.handler import Handler
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.opendart.report_code import ReportCode


class Opendart(Handler):
    TAG: str = 'opendart-005930'

    def handle(self):
        from fdap.app.opendart.opendart_service import OpenDartService
        params = self.get_parameters()
        stock_code = None
        stock_info = None

        if 'stock_code' in params:
            stock_code = params['stock_code']
        elif 'stock_info' in params:
            stock_info = params['stock_info']
        else:
            stock_code = '005930'

        if 'year' in params:
            year = params['year']
        else:
            year = '2021'

        if 'report_code' in params:
            report_code = params['report_code']
        else:
            report_code = ReportCode.Q1

        service = OpenDartService()
        collect = {}
        if stock_code:
            corp_code = service.get_corp_code_by_stock_code(stock_code)
            single_data = service.get_single(corp_code.corp_code, year, report_code)
            collect = single_data[stock_code]
        if stock_info:
            corp_codes = []
            for basic_info in stock_info:
                if isinstance(basic_info, BasicInfo):
                    corp_code = service.get_corp_code_by_stock_code(basic_info.code)
                    if corp_code is not None:
                        corp_codes.append(corp_code.corp_code)

            collect = service.get_multi(corp_codes, year, report_code)

        return collect
