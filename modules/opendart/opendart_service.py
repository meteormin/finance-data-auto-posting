from modules.opendart.opendart_client import OpenDartClient
from configparser import ConfigParser
from definitions import CONFIG_PATH
from modules.opendart.opendart_data import *
from modules.opendart.report_code import ReportCode
import xmltodict
import os
from typing import List, Dict, Union
from modules.utils.customlogger import CustomLogger


class OpenDartService:
    """
    Open Dart Api
    """
    Q1: str = ReportCode.Q1
    Q2: str = ReportCode.Q2
    Q3: str = ReportCode.Q3
    Q4: str = ReportCode.Q4
    QUARTERS: dict = ReportCode.__members__

    def __init__(self, url: str = None, api_key: str = None):
        """

        :param url: open dart api access url
        :param api_key: open dart api key
        """
        if url is None or api_key is None:
            self._config = ConfigParser()
            self._config.read(CONFIG_PATH + '/opendart.ini')
            url = self._config['api']['url']
            api_key = self._config['api']['api_key']

        self._client = OpenDartClient(host=url, api_key=api_key)
        self._logger = CustomLogger.logger('automatic-posting', __name__)
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

    def get_corp_code_by_stock_code(self, stock_code: str):
        for corp_code in self.get_corp_codes():
            if stock_code == corp_code.stock_code:
                return corp_code

    def get_single(self, corp_code: str, year: str, report_code: str) -> Union[Dict[str, List[Acnt]], None]:
        self._logger.debug('request get single corp accounts')
        single_acnt = self._client.get_single(corp_code, year, report_code)
        if self._client.is_success():
            self._logger.debug('success request')
        else:
            self._logger.warning('fail request: %s', self._client.get_error())

        single = None
        if isinstance(single_acnt, dict):
            if 'list' in single_acnt:
                single = self._div_by_stock(Acnt().map_list(single_acnt['list']))

        return single

    def get_multi(self, corp_codes: list, year: str, report_code: str) -> Dict[str, List[Acnt]]:
        self._logger.debug('request get multiple corp accounts')
        multi_acnt = self._client.get_multi(corp_codes, year, report_code)
        if self._client.is_success():
            self._logger.debug('success request')
        else:
            self._logger.warning('fail request: %s', self._client.get_error())

        multi = {}
        if isinstance(multi_acnt, dict):
            if 'list' in multi_acnt:
                multi = self._div_by_stock(Acnt().map_list(multi_acnt['list']))

        return multi

    def get_deficit_count(self, corp_code, year: str, count: int = 3):
        deficit_count = 0
        for i in range(count):
            for q in self.QUARTERS:
                acnt = self.get_single(corp_code, str(int(year) - i), q.value)
                for acnt_list in acnt.values():
                    for account in acnt_list:
                        if account.account_nm == '당기순이익':
                            if account.thstrm_amount is not None:
                                if int(account.thstrm_amount) < 0:
                                    deficit_count += 1
        return deficit_count

    @staticmethod
    def _div_by_stock(multi_acnt: List[Acnt]) -> Dict[str, List[Acnt]]:
        rs_dict = {}
        for acnt in multi_acnt:
            if acnt.stock_code:
                if acnt.stock_code not in rs_dict:
                    rs_dict[acnt.stock_code] = []
                rs_dict[acnt.stock_code].append(acnt)

        return rs_dict
