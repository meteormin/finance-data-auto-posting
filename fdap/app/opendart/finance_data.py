import dataclasses
from fdap.app.opendart.opendart_service import OpenDartService
from fdap.utils.data import BaseData
from typing import Dict
from fdap.app.opendart.opendart_data import AcntCollection
from fdap.utils.customlogger import CustomLogger
from fdap.utils.util import currency_to_int


@dataclasses.dataclass
class FinanceData(BaseData):
    date: str = None
    reprt_code: str = None
    current_assets: int = 0
    total_assets: int = 0
    floating_debt: int = 0
    total_debt: int = 0
    total_capital: int = 0
    net_income: int = 0
    deficit_count: int = 0
    flow_rate: float = 0.0
    debt_rate: float = 0.0
    pbr: float = 0.0
    per: float = 0.0
    roe: float = 0.0

    @staticmethod
    def get_map_table() -> Dict[str, Dict[str, str]]:
        return {
            'account_nm': {
                'current_assets': '유동자산',
                'total_assets': '자산총계',
                'floating_debt': '유동부채',
                'total_debt': '부채총계',
                'total_capital': '자본총계',
                'net_income': '당기순이익'
            }
        }

    def map(self, acnt: AcntCollection) -> __name__:
        """

        :param acnt: List[Acnt]
        :return FinanceData:
        """
        for key, name in self.get_map_table()['account_nm'].items():
            account = acnt.get_by_account_nm(account_nm=name, fs_div='CFS')
            if account is None:
                account = acnt.get_by_account_nm(account_nm=name, fs_div='OFS')

            self.date = account.thstrm_dt
            self.reprt_code = account.reprt_code
            self.__setattr__(key, currency_to_int(account.thstrm_amount))

            if '당기순' in account.account_nm.replace(' ', ''):
                od_service = OpenDartService()
                corp_code = od_service.get_corp_code_by_stock_code(account.stock_code)

                self.deficit_count = od_service.get_deficit_count(corp_code.corp_code, account.bsns_year)

        return self

    @staticmethod
    def __logger():
        return CustomLogger.logger('automatic-posting', __name__)

    def calculate_flow_rate(self):
        try:
            self.flow_rate = round(self.current_assets / self.floating_debt * 100, 2)
        except ZeroDivisionError:
            logger = self.__logger()
            logger.debug('flow_rate:{} / {} * 100'.format(self.current_assets, self.floating_debt))
            self.flow_rate = 0.0
        return self

    def calculate_debt_rate(self):
        try:
            self.debt_rate = round(self.total_debt / self.total_assets * 100, 2)
        except ZeroDivisionError:
            logger = self.__logger()
            logger.debug('debt_rate:{} / {} * 100'.format(self.total_debt, self.total_assets))
            self.debt_rate = 0.0
        return self

    def calculate_per(self, current_price: int, issue_cnt: int):
        try:
            self.per = round(current_price / (self.net_income / issue_cnt), 2)
        except ZeroDivisionError:
            logger = self.__logger()
            logger.debug('per:{} / ({} / {})'.format(current_price, self.net_income, issue_cnt))
            self.per = 0.0
        return self

    def calculate_pbr(self, current_price: int, issue_cnt: int):
        try:
            self.pbr = round(current_price / ((self.total_capital - self.total_debt) / issue_cnt), 2)
        except ZeroDivisionError:
            logger = self.__logger()
            logger.debug(
                'per:{} / (({} - {}) / {})'.format(current_price, self.total_capital, self.total_debt, issue_cnt))
            self.pbr = 0.0
        return self

    def calculate_roe(self):
        try:
            self.roe = round((self.net_income / self.total_capital) * 100, 2)
        except ZeroDivisionError:
            logger = self.__logger()
            logger.debug(
                'per:({} / {}) * 100'.format(self.net_income, self.total_capital))
            self.roe = 0.0
        return self
