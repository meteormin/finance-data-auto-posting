from fdap.app.contracts.service import Service
from fdap.app.opendart.report_code import ReportCode
from fdap.app.kiwoom.kiwoom_service import KiwoomService
from fdap.app.opendart.opendart_service import OpenDartService
from fdap.app.tistory.tistory_client import TistoryClient
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.refine.refine import Refine
from fdap.app.infographic.table import Table
from fdap.app.infographic.chart import Chart
from fdap.definitions import RESOURCE_PATH
from fdap.app.autopost.template import *
from fdap.app.repositories.post_repository import PostsRepository
from fdap.app.tistory.tistory_data import PostData
from fdap.app.tistory.tistory_data import PostDto
from fdap.utils.util import config_json
from fdap.app.tistory.tistory_data import LoginInfo
from typing import Dict, Union
import os


class AutoPost(Service):

    def __init__(
            self,
            kiwoom: KiwoomService,
            opendart: OpenDartService,
            tistory: TistoryClient,
            refine: Refine,
            repo: PostsRepository
    ):
        super().__init__()
        self.kiwoom = kiwoom
        self.opendart = opendart
        self.tistory = tistory
        self.refine = refine
        self.repo = repo

        config = config_json('tistory')
        api_config = config['api']
        kakao_config = config['kakao']

        login_info = LoginInfo(
            client_id=api_config['client_id'],
            client_secret=api_config['client_secret'],
            redirect_uri=api_config['redirect_uri'],
            response_type=api_config['response_type'],
            kakao_id=kakao_config['id'],
            kakao_password=kakao_config['password'],
            state=api_config['state']
        )

        self.tistory.login(login_info)
        self.tistory.apis().post().access_token = self.tistory.access_token

    def make_data(self, sector: str, year: str, q: ReportCode):
        stock_list = self.kiwoom.get_stock_list_by_sector(sector)

        corp_codes = []
        for basic_info in stock_list:
            if isinstance(basic_info, BasicInfo):
                corp_code = self.opendart.get_corp_code_by_stock_code(basic_info.code)
                if corp_code is not None:
                    corp_codes.append(corp_code.corp_code)

        collect = self.opendart.get_multi(corp_codes, year, q)

        refine_collection = self.refine.refine_multiple(stock_list, collect)
        table = Table(refine_collection)
        df = table.make_dataframe()

        if df is None:
            return None

        table_file_path = os.path.join(RESOURCE_PATH, f'{sector}_{year}_{q}_table.png')
        chart_dict = {}
        if table.save_img(table_file_path):
            chart = Chart(df)
            y_label = chart.get_ko_col_names()
            y_label.pop('rank')
            y_label.pop('stock_name')
            y_label.pop('stock_code')

            for key, ko in y_label.items():
                chart_file_path = os.path.join(RESOURCE_PATH, f'{sector}_{year}_{q}_{key}_chart.png')
                if chart.save_img(chart_file_path, '종목명', ko):
                    chart_dict[ko] = chart_file_path
        return {
            'table': table_file_path,
            'chart': chart_dict
        }

    def _upload_file(self, file_path: str):
        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            contents = f.read()
            res = self.tistory.apis().post().attach(filename, contents)
            return res['tistory']['url']

    def post(self, upload_files: Dict[str, Union[str, list]]) -> dict:
        img_url = {
            'table': None,
            'chart': []
        }
        if 'table' in upload_files:
            table = upload_files['table']
            img_url['table'] = self._upload_file(table)

        if 'chart' in upload_files:
            chart_list = upload_files['chart']
            for chart in chart_list:
                img_url['chart'].append(self._upload_file(chart))

        return img_url

    def auto(self):
        sector_name = '전기전자'
        sector = '013'
        year = '2021'
        report_code = ReportCode.Q1

        exist_post = self.repo.find_by_sector(sector, year, report_code.value)
        if exist_post:
            return None

        data = self.make_data(sector, year, report_code)
        urls = self.post(data)
        subject = make_template(sector_name, year, ReportCode.get_index(report_code.value))

        table = urls['table']
        contents = make_img_tag(f'{sector_name} 상위 10개 종목', table)

        for ko, chart in urls['chart'].items():
            contents += make_img_tag(f'{sector_name}: {ko}', chart)

        post = PostData(
            title=subject,
            content=contents,
            visibility=0
        )

        post_dto = PostDto(title=subject, content=contents)
        post_dto.sector = sector
        post_dto.report_code = report_code
        post_dto.year = year

        self.repo.create(post_dto)
        return self.tistory.apis().post().write(post)
