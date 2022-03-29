from koapy import KiwoomOpenApiPlusEntrypoint
from fdap.app.kiwoom.stock_info import StockInfo
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.contracts.logging import Logging
from typing import List


class KoapyWrapper(Logging):
    """KoapyWrapper is just wrapping koapy for me

    Attributes:
        koapy: koapy
    """
    _koapy: KiwoomOpenApiPlusEntrypoint

    def __init__(self):
        super().__init__()
        self._koapy = None
        self._logger.info('init: %s', __name__)
        self._logger.info('Auto Login')
        self.connect()
        self._logger.info('Success Login')

    def __del__(self):
        self.disconnect()

    def _create_koapy(self):
        self._koapy = KiwoomOpenApiPlusEntrypoint()

    def connect(self):
        if not isinstance(self._koapy, KiwoomOpenApiPlusEntrypoint):
            self._create_koapy()
        if not self.get_connect_state():
            self._koapy.EnsureConnected()

    def disconnect(self):
        if self.get_connect_state():
            self._logger.debug('close Koapy')
            self._koapy.close()

    def get_connect_state(self) -> bool:
        """can you check login
        Returns
            bool:
        """
        self._logger.debug('Check Login...')

        try:
            return bool(self._koapy.GetConnectState())
        except ValueError as e:
            self._logger.warning(e)
            del self._koapy
            self._create_koapy()
            return False

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
            list: [<Stockinfo>]
        """

        # 업종 리스트를 가져온다.
        sectors = self.get_sector_list()

        # 현재 입력 받은 업종의 개수를 찾아 limit(으)로 설정
        limit = 0
        for s in sectors:
            if sector == s['code']:
                limit = int(s['count'])

        screenno = '2002'

        inputs = {
            '시장구분': market_code,
            '업종코드': sector
        }

        rqname = '업종별주가요청'
        trcode = 'OPT20002'

        multi = []

        # 현재 조회된 업종의 개수가 limit보다 크면 강제 종료 후 break
        cnt = 0
        for event in self.transaction_call(rqname, trcode, screenno, inputs):
            if cnt > limit:
                self.disconnect()
                self.connect()
                break
            self._logger.debug('Get event for request: {}'.format(rqname))
            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            for value in multi_values:
                temp_dict = {}
                stock_info = StockInfo()
                for n, v in zip(multi_names, value.values):
                    temp_dict[n] = v

                multi.append(stock_info.map(temp_dict))
                self._logger.debug('stock_code: {}, count: {}'.format(stock_info.code, cnt))
                cnt += 1

        return multi

    def get_sector_info_as_list(self, sector: str, market_code='0'):

        screenno = '2001'

        inputs = {
            '시장구분': market_code,
            '업종코드': sector
        }

        rqname = '업종현재가요청'
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
            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            for value in multi_values:
                temp_dict = {}
                for n, v in zip(multi_names, value.values):
                    if n == '종목코드':
                        temp_dict['code'] = v
                    if n == '종목명':
                        temp_dict['name'] = v
                    if n == '상장종목수':
                        temp_dict['count'] = v

                multi.append(temp_dict)

        return multi
