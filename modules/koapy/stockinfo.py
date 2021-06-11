from modules.lib.string import Str


class StockInfo:
    """
    StockInfo: stock information

    Args:
        code (str): stock code
        name (str): stock name
        currentPrice (str): stock current price

    Attributes
        _code (str): stock code
        _name (str): stock name
        _currentPrice (int): stock current price
    """

    def __init__(self, code='', name='', current_price='0'):

        self.code = code
        self.name = name
        self.current_price = current_price

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
        self._code = str(code)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = str(name)

    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, current_price: str):
        self._current_price = int(current_price)

    def to_dict(self):
        """StockInfo to dictionary
        you can __dict__ but, this class has private proerties
        so, if you use __dict__ then returns dictionary key is '_propertyname'
        I felt not good... 
        so, I define this method

        Returns:
            dict: to convert to json
        """
        dt = self.__dict__

        rs = {}
        for k, v in dt.items():
            name = k.replace('_', '')
            rs[Str.snake(name)] = v

        return rs

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
