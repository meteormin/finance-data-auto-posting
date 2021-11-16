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
from fdap.app.autopost.parameters import Parameters
from fdap.app.autopost.rotation import RotationSector
from fdap.utils.util import get_quarter
from typing import Dict, Union, List
from datetime import datetime
import os


class AutoPost(Service):
    _kiwoom: KiwoomService
    _opendart: OpenDartService
    _tistory: TistoryClient
    _refine: Refine
    _repo: PostsRepository

    def __init__(
            self,
            kiwoom: KiwoomService,
            opendart: OpenDartService,
            tistory: TistoryClient,
            refine: Refine,
            repo: PostsRepository
    ):
        super().__init__()
        self._kiwoom = kiwoom
        self._opendart = opendart
        self._tistory = tistory
        self._refine = refine
        self._repo = repo

    def __del__(self):
        self.close()

    def close(self):
        self._kiwoom.disconnect()

    def _make_data(self, sector: str, year: str, q: ReportCode):
        self._logger.debug('make_data')
        stock_list = self._kiwoom.get_stock_list_by_sector(sector)
        self._logger.debug('stock_list: ' + str(len(stock_list)))

        corp_codes = []
        for basic_info in stock_list:
            if isinstance(basic_info, BasicInfo):
                corp_code = self._opendart.get_corp_code_by_stock_code(basic_info.code)
                if corp_code is not None:
                    corp_codes.append(corp_code.corp_code)

        collect = self._opendart.get_multi(corp_codes, year, q)
        self._logger.debug(f"finance_data: {str(len(collect))}")

        refine_collection = self._refine.refine_multiple(stock_list, collect)
        self._logger.debug(f"refine_data: {str(refine_collection.count())}")

        table = Table(refine_collection)
        df = table.make_dataframe()

        if df is None:
            self._logger.debug('make_data is None')
            return None

        table_file_path = os.path.join(RESOURCE_PATH, f'{sector}_{year}_{q.value}_table.png')
        chart_dict = {}
        if table.save_img(table_file_path):
            chart = Chart(df)
            y_label = chart.get_ko_col_names()
            # y_label.pop('rank')
            y_label.pop('stock_name')
            y_label.pop('stock_code')

            for key, ko in y_label.items():
                chart_file_path = os.path.join(RESOURCE_PATH, f'{sector}_{year}_{q.value}_{key}_chart.png')
                if chart.save_img(chart_file_path, '종목명', ko):
                    chart_dict[ko] = chart_file_path
        return {
            'table': table_file_path,
            'chart': chart_dict
        }

    def _blog_login(self, platform: str = 'tistory'):
        config = config_json(platform)
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

        self._tistory.login(login_info)
        self._tistory.apis().post().access_token = self._tistory.access_token

    def _upload_file(self, file_path: str):
        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            contents = f.read()
            res = self._tistory.apis().post().attach(filename, contents)
            return res['tistory']['url']

    def _upload_images(self, upload_files: Dict[str, Union[str, Union[str, dict]]]) -> dict:
        self._logger.debug('ready for post')
        img_url = {
            'table': None,
            'chart': {}
        }

        if 'table' in upload_files:
            table = upload_files['table']
            img_url['table'] = self._upload_file(table)

        if 'chart' in upload_files:
            chart_dict = upload_files['chart']
            for ko, chart in chart_dict.items():
                img_url['chart'][ko] = self._upload_file(chart)

        return img_url

    def run(self, parameters: Parameters) -> Union[None, dict]:
        self._logger.debug(f"Parameters: {parameters.to_json()}")

        sector_name = parameters.sector_name
        sector = parameters.sector_code
        year = parameters.year
        report_code = ReportCode.get_by_index(parameters.quarter)

        exist_post = self._repo.find_by_sector(sector, year, report_code.value)
        self._logger.debug(exist_post)
        if exist_post:
            return None

        data = self._make_data(sector, year, report_code)

        self._blog_login(platform='tistory')

        urls = self._upload_images(data)

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

        post_api = self._tistory.apis().post()
        res = post_api.write(post)

        post_dto = PostDto(title=subject, content=contents)
        post_dto.sector = sector
        post_dto.report_code = report_code.value
        post_dto.year = year

        if post_api.is_success():
            post_dto.url = res['tistory']['url']
            post_dto.is_success = True
        else:
            post_dto.url = None
            post_dto.is_success = False

        return self._repo.create(post_dto)

    @staticmethod
    def _make_parameters(rotator: RotationSector) -> Parameters:
        date = datetime.now()
        quarter = get_quarter(date) - 1
        report_code = ReportCode.get_by_index(quarter)
        sector = rotator.get_sector(str(date.year), report_code.value)

        return Parameters(
            sector_code=sector['code'],
            sector_name=sector['name'],
            year=str(date.year),
            quarter=quarter
        )

    def auto(self, sector_list: List[dict] = None, rules: dict = None) -> Union[None, dict]:
        if sector_list is None or len(sector_list) == 0:
            sector_list = self._kiwoom.get_sector_list()

        rotator = RotationSector(self._repo, sector_list, rules)
        parameter = self._make_parameters(rotator)

        return self.run(parameter)
