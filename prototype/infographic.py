from prototype.handler import Handler
from os.path import exists
from fdap.app.refine.refine_data import RefineData
from fdap.app.opendart.finance_data import FinanceData
from fdap.app.kiwoom.basic_info import BasicInfo


class Infographic(Handler):
    TAG: str = 'infographic'

    def get_refine_data(self) -> RefineData:
        refine_data = RefineData()
        refine_data.finance_data = self.get_finance_data()
        refine_data.basic_info = self.get_basic_info()
        return refine_data

    @staticmethod
    def get_finance_data() -> FinanceData:
        fd = FinanceData()
        fd.roe = 2.6
        fd.flow_rate = 232.11
        fd.debt_rate = 30.18
        fd.deficit_count = 0
        fd.per = 58.6
        fd.pbr = 2.69
        return fd

    @staticmethod
    def get_basic_info() -> BasicInfo:
        bi = BasicInfo()
        bi.capital = 4184818
        bi.code = '005930'
        bi.name = '삼성전자'
        bi.current_price = 71500
        return bi

    def handle(self):
        from prototype.refine import Refine
        from fdap.app.infographic.table import Table
        from fdap.app.infographic.chart import Chart
        from fdap.definitions import ROOT_DIR

        rs_dict = {
            'table': None,
            'chart': None
        }

        refine_data = Refine(self._save_result).handle()
        # refine_data = self.get_refine_data()
        table = Table(refine_data)
        table_file_path = ROOT_DIR + '/../prototype/results/infographic-table.png'

        if table.save_img(table_file_path):
            rs_dict['table'] = table_file_path

        chart = Chart(table.make_dataframe())
        y_label = chart.get_ko_col_names()
        y_label.pop('rank')
        y_label.pop('stock_name')
        y_label.pop('stock_code')

        chart_list = []
        for key, ko in y_label.items():
            chart_file_path = '{project_dir}/../prototype/results/infographic-chart_{label}.png'.format(
                project_dir=ROOT_DIR, label=key)
            if chart.save_img(chart_file_path, '종목명', ko):
                chart_list.append(chart_file_path)

        rs_dict['chart'] = chart_list

        return rs_dict
