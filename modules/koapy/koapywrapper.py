from koapy import KiwoomOpenApiPlusEntrypoint
import logging
from modules.koapy.stockinfo import StockInfo
from modules.koapy.basicinfo import BasicInfo

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d',
    level=logging.DEBUG)


class KoapyWrapper:
    """KoapyWrapper is just wrapping koapy for me

    Attributes:
        koapy: koapy
    """

    def __init__(self):
        self._koapy = KiwoomOpenApiPlusEntrypoint()
        logging.info('Auto Login')
        self._koapy.EnsureConnected()
        logging.info('Success Login')

    def getConnectState(self):
        """can you check login
        Returns
            bool: maybe?
        """
        logging.info('Check Login...')
        return self._koapy.GetConnectState()

    def koapy(self):
        """get koapy
        Returns:
            KiwoomOpenApiPlusEntrypoint: ...
        """
        return self._koapy

    def getCodeListByMarketAsList(self, marketCode: str):
        """get codes of stock by market code
        Args:
            marketCode (str): market code 0: 'kospi' 1: 'kosdaq' etc...
        Returns:
            dict: {'names':[...],'codes':[...]}
        """
        codes = self._koapy.GetCodeListByMarketAsList(marketCode)
        names = [self._koapy.getMasterCodeName(code) for code in codes]

        return {
            'names': names,
            'codes': codes
        }

    def getStockBasicInfoAsDict(self, code: str):
        """get stock basic info
        Args:
            code (str): stock code
        Returns:
            dict: ... ref: 'koapy get stockinfo -h'
        """
        basicDict = self._koapy.GetStockBasicInfoAsDict(code)
        basicInfo = BasicInfo()

        return basicInfo.map(basicDict).toDict()

    def getDailyStockDataAsDataFrame(self, code: str):
        """ get daily stock data
        Args:
            code (str): stock code
        Returns:
            Pandas.dataframe:

        """
        return self._koapy.GetDailyStockDataAsDataFrame(code)

    def getThemeGroupListAsDict(self):
        themeGroup = self._koapy.GetThemeGroupList(1)
        return self.parseRawAsDictList(themeGroup)

    def getThemeGroupCodeAsList(self, themeCode):
        themeCodeList = self._koapy.GetThemeGroupCode(themeCode)
        return themeCodeList.split(';')

    def parseRawAsDictList(self, raw):
        ls = raw.split(';')

        rsList = []
        for i in ls:
            [code, name] = i.split('|')

            rsDict = {}
            rsDict['code'] = code
            rsDict['name'] = name
            rsList.append(rsDict)

        return rsList

    def transactionCall(self, rqname: str, trcode: str, screenno: str, inputs):
        """call transaction(tr)
        Args:
            rqname (str): request name
            trcode (str): transaction code
            screenno (str): can input any 4digit numbers but don't input zero
            inputs (str): input parameter ref 'koapy get trinfo -t {trcode}'
        Returns:
            I'm not sure
        """
        return self._koapy.TransactionCall(rqname, trcode, screenno, inputs)

    def getStockInfoBySectorAsList(self, sector: str, marketCode='0'):
        """get stock info by sector using transaction call
        Args:
            sector (str): sector code
            marketCode (str): market code, default='0'
        Returns:
            list: [<stockinfo>]
        """
        screenno = '2002'

        inputs = {
            '시장구분': marketCode,
            '업종코드': sector
        }

        rqname = '업종별주가'
        trcode = 'OPT20002'

        multi = []
        for event in self.transactionCall(rqname, trcode, screenno, inputs):
            names = event.single_data.names

            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            stockinfo = StockInfo()
            for value in multi_values:
                temp_dict = {}
                for n, v in zip(names, value.values):
                    temp_dict[n] = v
                multi.append(stockinfo.map(temp_dict).toDict())

        return multi

    def getSectorInfoAsList(self, sector: str, marketCode='0'):

        screenno = '2001'

        inputs = {
            '시장구분': marketCode,
            '업종코드': sector
        }

        rqname = '업종별월봉조회'
        trcode = 'OPT20001'

        multi = []
        for event in self.transactionCall(rqname, trcode, screenno, inputs):
            names = event.single_data.names

            multi_names = event.multi_data.names
            multi_values = event.multi_data.values

            stockinfo = StockInfo()
            for value in multi_values:
                temp_dict = {}
                for n, v in zip(names, value.values):
                    temp_dict[n] = v
                multi.append(stockinfo.map(temp_dict).toDict())

        return multi
