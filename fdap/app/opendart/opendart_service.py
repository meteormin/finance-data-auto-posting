import xmltodict
import os
from fdap.app.opendart.opendart_client import OpenDartClient
from fdap.app.opendart.opendart_data import *
from fdap.utils.util import config_json, currency_to_int
from fdap.app.opendart.report_code import ReportCode
from fdap.app.contracts.service import Service
from typing import List, Dict, Union
from configparser import ConfigParser


class OpenDartService(Service):
    """
    Open Dart Api
    """
    Q1: ReportCode.Q1 = ReportCode.Q1
    Q2: ReportCode.Q2 = ReportCode.Q2
    Q3: ReportCode.Q3 = ReportCode.Q3
    Q4: ReportCode.Q4 = ReportCode.Q4
    QUARTERS: dict = ReportCode.__members__
    _config: Union[ConfigParser, dict]
    _client: OpenDartClient

    def __init__(self, url: str = None, api_key: str = None):
        """

        :param url: open dart api access url
        :param api_key: open dart api key
        """
        super().__init__()
        if url is None or api_key is None:
            self._config = config_json('opendart')
            url = self._config['api']['url']
            api_key = self._config['api']['api_key']

        self._client = OpenDartClient(host=url, api_key=api_key)
        self._logger.info('init: %s', __name__)

    def get_corp_codes(self) -> List[CorpCode]:
        """
        상장기업들의 고유코드 가져오기

        :return: List[CorpCode]
        """
        filename = 'CORPCODE.xml'
        self._logger.debug('get corp codes')
        if os.path.isfile(filename):
            self._logger.debug('exists CORPCODE.xml')
            with open(filename, 'r', encoding='utf-8') as f:
                corp_code_xml = f.read()
                corp_code_dict = xmltodict.parse(corp_code_xml).get('result').get('list')
        else:
            self._logger.debug('request open dart get corp-codes...')
            corp_code_dict = self._client.get_corp_codes()
            if self._client.is_success():
                self._logger.debug('success request')
            else:
                self._logger.warning('fail request: %s', self._client.get_error())

        return CorpCode().map_list(corp_code_dict)

    def get_corp_code_by_stock_code(self, stock_code: str) -> Union[CorpCode, None]:
        for corp_code in self.get_corp_codes():
            if stock_code == corp_code.stock_code:
                return corp_code
        return None

    def get_single(self, corp_code: str, year: str, report_code: ReportCode) -> Union[Dict[str, AcntCollection], None]:
        self._logger.debug('request get single corp accounts')
        single_acnt = self._client.get_single(corp_code, year, report_code.value)
        if self._client.is_success():
            self._logger.debug('success request')
            self._logger.debug('corp_code: ' + corp_code)
        else:
            self._logger.warning('fail request: %s', self._client.get_error())

        single = None
        if isinstance(single_acnt, dict):
            if 'list' in single_acnt:
                single = self._div_by_stock(Acnt().map_list(single_acnt['list']))

        return single

    def get_multi(self, corp_codes: list, year: str, report_code: ReportCode) -> Dict[str, AcntCollection]:
        self._logger.debug('request get multiple corp accounts')
        multi_acnt = self._client.get_multi(corp_codes, year, report_code.value)
        if self._client.is_success():
            self._logger.debug('success request')
            self._logger.debug('corp_codes' + str(corp_codes))
        else:
            self._logger.warning('fail request: %s', self._client.get_error())

        multi = {}
        if isinstance(multi_acnt, dict):
            if 'list' in multi_acnt:
                multi = self._div_by_stock(Acnt().map_list(multi_acnt['list']))

        return multi

    def get_deficit_count(self, corp_code: str, year: str, count: int = 3):
        deficit_count = 0
        for i in range(count):
            for q in self.QUARTERS.values():
                acnt = self.get_single(corp_code, str(int(year) - i), q)
                if acnt is not None:
                    for acnt_collect in acnt.values():
                        account = acnt_collect.get_by_account_nm('당기순')
                        if account is not None:
                            if account.thstrm_amount is not None:
                                if currency_to_int(account.thstrm_amount) < 0:
                                    deficit_count += 1
        return deficit_count

    @staticmethod
    def _div_by_stock(multi_acnt: List[Acnt]) -> Dict[str, AcntCollection]:
        rs_dict = {}
        for acnt in multi_acnt:
            if acnt.stock_code:
                if acnt.stock_code not in rs_dict:
                    rs_dict[acnt.stock_code] = AcntCollection()
                rs_dict[acnt.stock_code].push(acnt)

        return rs_dict
