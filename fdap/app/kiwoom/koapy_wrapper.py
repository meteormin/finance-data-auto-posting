from koapy import KiwoomOpenApiPlusEntrypoint
from fdap.app.kiwoom.stock_info import StockInfo
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.app.utils.customlogger import CustomLogger
from typing import List


class KoapyWrapper:
    """KoapyWrapper is just wrapping koapy for me

    Attributes:
        koapy: koapy
    """
    _koapy: KiwoomOpenApiPlusEntrypoint

    def __init__(self):
        self._koapy = KiwoomOpenApiPlusEntrypoint()
        self._logger = CustomLogger.logger('automatic-posting', __name__)
        self._logger.info('init: %s', __name__)
        self._logger.info('Auto Login')
        self._koapy.EnsureConnected()
        self._logger.info('Success Login')

    def connect(self):
        self._koapy.EnsureConnected()

    def get_connect_state(self):
        """can you check login
        Returns
            bool: maybe?
        """
        self._logger.debug('Check Login...')
        return self._koapy.GetConnectState()

    def koapy(self):
        """get koapy
        Returns:
            KiwoomOpenApiPlusEntrypoint: ...
        """
        return self._koapy

    def get_code_list_by_market_as_list(self, market_code: str):
        """get codes of stock by market code
        Args:
            market_code (str): market code 0: 'kospi' 1: 'kosdaq' etc...
        Returns:
            dict: {'names':[...],'codes':[...]}
        """
        codes = self._koapy.GetCodeListByMarketAsList(market_code)
        names = [self._koapy.getMasterCodeName(code) for code in codes]

        return {
            'names': names,
            'codes': codes
        }

    def get_stock_basic_info_as_dict(self, code: str) -> BasicInfo:
        """get stock basic info
        Args:
            code (str): stock code
        Returns:
            dict: ... ref: 'koapy get stockinfo -h'
        """
        basic_dict = self._koapy.GetStockBasicInfoAsDict(code)
        basic_info = BasicInfo()

        return basic_info.map(basic_dict)

    def get_daily_stock_data_as_data_frame(self, code: str):
        """ get daily stock data
        Args:
            code (str): stock code
        Returns:
            Pandas.dataframe:

        """
        return self._koapy.GetDailyStockDataAsDataFrame(code)

    def get_theme_group_list_as_dict(self):
        theme_group = self._koapy.GetThemeGroupList(1)
        return self.parse_raw_as_dict_list(theme_group)

    def get_theme_group_code_as_list(self, theme_code):
        theme_code_list = self._koapy.GetThemeGroupCode(theme_code)
        return theme_code_list.split(';')

    @staticmethod
    def parse_raw_as_dict_list(raw):
        ls = raw.split(';')

        rs_list = []
        for i in ls:
            [code, name] = i.split('|')

            rs_dict = {'code': code, 'name': name}
            rs_list.append(rs_dict)

        return rs_list

    def transaction_call(self, rqname: str, trcode: str, screenno: str, inputs):
        """call transaction(tr)
        Args:
            rqname (str): request name
            trcode (str): transaction code
            screenno (str): can input any 4digit numbers but don't input zero
            inputs (dict): input parameter ref 'koapy get trinfo -t {trcode}'
        Returns:
            I'm not sure
        """
        return self._koapy.TransactionCall(rqname, trcode, screenno, inputs)

    def get_stock_info_by_sector_as_list(self, sector: str, market_code='0') -> List[StockInfo]:
        """get stock info by sector using transaction call
        Args:
            sector (str): sector code
            market_code (str): market code, default='0'
        Returns:
            list: [<stockinfo>]
        """
        screenno = '2002'

        inputs = {
            '시장구분': market_code,
            '업종코드': sector
        }

        rqname = '업종별주가'
        trcode = 'OPT20002'

        multi = []
        for event in self.transaction_call(rqname, trcode, screenno, inputs):
            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            for value in multi_values:
                temp_dict = {}
                stock_info = StockInfo()
                for n, v in zip(multi_names, value.values):
                    temp_dict[n] = v
                multi.append(stock_info.map(temp_dict))

        return multi

    def get_sector_info_as_list(self, sector: str, market_code='0'):

        screenno = '2001'

        inputs = {
            '시장구분': market_code,
            '업종코드': sector
        }

        rqname = '업종별월봉조회'
        trcode = 'OPT20001'

        multi = []
        for event in self.transaction_call(rqname, trcode, screenno, inputs):
            names = event.single_data.names

            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            for value in multi_values:
                temp_dict = {}
                for n, v in zip(names, value.values):
                    temp_dict[n] = v
                multi.append(temp_dict)

        return multi

    def get_sector_list(self):

        screenno = '2003'

        inputs = {
            '업종코드': '001'
        }

        rqname = '전업종지수요청'
        trcode = 'OPT20003'

        multi = []
        for event in self.transaction_call(rqname, trcode, screenno, inputs):
            names = event.single_data.names

            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            for value in multi_values:
                temp_dict = {}
                for n, v in zip(names, value.values):
                    if n == '종목코드':
                        temp_dict['code'] = v
                    if n == '종목명':
                        temp_dict['name'] = v

                multi.append(temp_dict)

        return multi
