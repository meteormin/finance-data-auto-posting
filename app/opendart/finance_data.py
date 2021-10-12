import dataclasses
from app.opendart.opendart_service import OpenDartService
from app.utils.data import BaseData
from typing import Dict
from app.opendart.opendart_data import AcntCollection


@dataclasses.dataclass
class FinanceData(BaseData):
    date: str = None
    reprt_code: str = None
    current_assets: int = 0
    total_assets: int = 0
    floating_debt: int = 0
    total_debt: int = 0
    net_income: int = 0
    flow_rate: int = 0
    debt_rate: int = 0
    deficit_count: int = 0

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
            account = acnt.get_by_account_nm(name)
            if account is not None:
                self.date = account.thstrm_dt
                self.reprt_code = account.reprt_code
                self.__setattr__(key, int(account.thstrm_amount.replace(',', '')))

                if account.account_nm == '당기순이익':
                    od_service = OpenDartService()
                    corp_code = od_service.get_corp_code_by_stock_code(account.stock_code)

                    self.deficit_count = od_service.get_deficit_count(corp_code, account.bsns_year)

            self._calculate_flow_rate()
            self._calculate_debt_rate()

        return self

    def _calculate_flow_rate(self):
        if self.floating_debt == 0:
            self.flow_rate = 0
            return
        self.flow_rate = int(self.current_assets / self.floating_debt * 100)

    def _calculate_debt_rate(self):
        if self.total_assets == 0:
            self.flow_rate = 0
            return
        self.debt_rate = int(self.total_debt / self.total_assets * 100)
