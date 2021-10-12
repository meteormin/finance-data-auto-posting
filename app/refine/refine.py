from typing import List
from app.refine.refine_data import *
from app.contracts.service import Service


class Refine(Service):

    def __init__(self):
        super().__init__()

        self._basic_info = []
        self._acnt = []
        self._refine_data = []
        self._logger.info('init: %s', __name__)

    def refine(self, basic_info: List[BasicInfo], acnt: Dict[str, AcntCollection]) -> List[RefineData]:
        self._basic_info = basic_info
        self._acnt = acnt

        for stock in basic_info:
            self._refine_data.append(self.refine_single(stock, acnt[stock.code]))
        return self.get_refined_data()

    @staticmethod
    def refine_single(basic_info: BasicInfo, acnt: AcntCollection) -> RefineData:
        refine_data = RefineData()

        refine_data.basic_info = basic_info

        finance_data = FinanceData()
        refine_data.finance_data = finance_data.map(acnt)

        return refine_data

    def get_refined_data(self) -> List[RefineData]:
        return self._refine_data
