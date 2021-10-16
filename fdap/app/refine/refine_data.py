import dataclasses
from fdap.app.utils.data import BaseData, BaseCollection
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.opendart.finance_data import FinanceData
from fdap.app.contracts.convertible import TableData
from typing import List


@dataclasses.dataclass
class RefineData(BaseData, TableData):
    basic_info: BasicInfo = None
    finance_data: FinanceData = None
    ASC = True
    DESC = False

    def to_dict(self):
        return {
            'stock_code': self.basic_info.code,
            'stock_name': self.basic_info.name,
            'current_price': self.basic_info.current_price,
            'market_cap': self.basic_info.capital,
            'deficit_count': self.finance_data.deficit_count,
            'per': self.finance_data.per,
            'pbr': self.finance_data.pbr,
            'roe': self.finance_data.roe,
            'flow_rate': self.finance_data.flow_rate,
            'debt_rate': self.finance_data.debt_rate
        }

    def sort_attr(self) -> dict:
        return {
            'market_cap': self.DESC,
            'deficit_count': self.ASC,
            'per': self.ASC,
            'pbr': self.ASC,
            'roe': self.DESC,
            'flow_rate': self.DESC,
            'debt_rate': self.ASC
        }


class RefineCollection(BaseCollection, TableData):
    ASC = True
    DESC = False

    _item: List[RefineData]

    def __init__(self, refine_list: List[RefineData]):
        self._item = refine_list

    def push(self, item: RefineData):
        self._item.append(item)
        return self

    def to_dict(self) -> List[dict]:
        rs_list = []
        for item in self._item:
            if isinstance(item, RefineData):
                rs_list.append(item.to_dict())

        return rs_list

    def sort_attr(self) -> dict:
        return {
            'market_cap': self.DESC,
            'deficit_count': self.ASC,
            'per': self.ASC,
            'pbr': self.ASC,
            'roe': self.DESC,
            'flow_rate': self.DESC,
            'debt_rate': self.ASC
        }
