import dataclasses
from app.utils.data import BaseData
from app.kiwoom.basic_info import BasicInfo
from app.opendart.finance_data import FinanceData


@dataclasses.dataclass
class RefineData(BaseData):
    basic_info: BasicInfo = None
    finance_data: FinanceData = None
