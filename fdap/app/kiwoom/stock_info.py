from dataclasses import dataclass
from fdap.app.utils.data import BaseData


@dataclass
class StockInfo(BaseData):
    code: str = None
    name: str = None
    current_price: str = None

    def map(self, data: dict):
        """ mapping for kiwoom response to stockinfo
        Args:
            data (list): received list
        Returns:
            self
        """
        if isinstance(data, dict):
            self.code = data['종목코드']
            self.name = data['종목명']
            self.current_price = data['현재가']
        return self
