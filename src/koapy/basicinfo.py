import dataclasses
from src.utils.data import BaseData


@dataclasses.dataclass
class BasicInfo(BaseData):
    """
    capital(시가총액) 단위: 억원
    """
    code: str = None
    name: str = None
    capital: int = 0
    per: int = 0
    roe: int = 0
    pbr: int = 0
    current_price: int = 0

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
            self.capital = int(data['시가총액'])
            self.per = data['PER']
            self.roe = data['ROE']
            self.pbr = data['PBR']
            self.current_price = int(data['현재가']) if int(data['현재가']) > 0 else int(data['현재가']) * -1
        return self
