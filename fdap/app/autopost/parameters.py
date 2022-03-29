from fdap.app.autopost.rotation import StockCondition
from fdap.utils.data import BaseData
from dataclasses import dataclass


@dataclass
class Parameters(BaseData):
    sector_name: str
    sector_code: str
    year: str
    quarter: int
    stock_condition: StockCondition
