from fdap.prototype.handler import Handler
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.opendart.report_code import ReportCode
from fdap.definitions import ROOT_DIR


class Opendart(Handler):
    TAG: str = 'opendart-005930'

    def handle(self):
        from fdap.app.opendart.opendart_service import OpenDartService
        from pandas import DataFrame

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
            if isinstance(report_code, str):
                report_code = ReportCode.get_by_str(report_code)
        else:
            report_code = ReportCode.Q1

        service = OpenDartService()
        collect = {}
        if stock_code:
            corp_code = service.get_corp_code_by_stock_code(stock_code)
            single_data = service.get_single(corp_code.corp_code, year, report_code)
            collect = single_data
        if stock_info:
            corp_codes = []
            for basic_info in stock_info:
                if isinstance(basic_info, BasicInfo):
                    corp_code = service.get_corp_code_by_stock_code(basic_info.code)
                    if corp_code is not None:
                        corp_codes.append(corp_code.corp_code)

            collect = service.get_multi(corp_codes, year, report_code)

        for stock, c in collect.items():
            df = DataFrame.from_records(c.to_dict())
            df.to_excel(ROOT_DIR + '/prototype/results/' + stock + '.xlsx')

        return collect
