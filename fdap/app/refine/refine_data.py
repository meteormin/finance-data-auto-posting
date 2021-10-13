import dataclasses
from fdap.app.utils.data import BaseData
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.opendart.finance_data import FinanceData


@dataclasses.dataclass
class RefineData(BaseData):
    basic_info: BasicInfo = None
    finance_data: FinanceData = None
