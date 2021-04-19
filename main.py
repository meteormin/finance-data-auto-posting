from modules.koapy.koapywrapper import KoapyWrapper
from modules.client.client import Client
import json
import time
import sys
import getopt


# main func
def main(market: str, sector=None):
    sectors = getSectors(market)
    results = []
    sectorDict = {}

    if(sector):
        sectorDict['code'] = sector
        sectorDict['name'] = sectors['sectors_raw'][sector]
        sectorDict['data'] = getStockInfoBySector(market, sector)
        tempList = []
        for stock in sectorDict['data']:
            basic = getStockBasicInfo(stock['code'])
            tempList.append(basic)
            time.sleep(0.1)
        sectorDict['data'] = tempList
        results.append(sectorDict)

    else:
        for s in sectors['sectors']:
            sectorDict['code'] = s['code']
            sectorDict['name'] = s['name']
            sectorDict['data'] = getStockInfoBySector(market, s['code'])

            tempList = []
            for stock in sectorDict['data']:
                basic = getStockBasicInfo(stock['code'])
                tempList.append(basic)
                time.sleep(0.1)
            sectorDict['data'] = tempList
            results.append(sectorDict)

    return sendStockInfo(results)


# 섹터 정보 가져오기
def getSectors(market: str):
    sectors = req.getSectors(market)

    return sectors


# 섹터 별 주가정보
def getStockInfoBySector(market: str, sector: str):
    sectorList = []

    if(market == 'kospi'):
        market = '0'
    elif(market == 'kosdaq'):
        market = '1'

    if(sector == None):
        sectorList = koapy.getStockInfoBySectorAsList('013', market)
    else:
        sectorList = koapy.getStockInfoBySectorAsList(sector, market)

    return sectorList


def getStockBasicInfo(code: str):
    return koapy.getStockBasicInfoAsDict(code)


def getSectorInfo(market: str, sector: str):
    sectorInfo = []

    if(market == 'kospi'):
        market = '0'
    elif(market == 'kosdaq'):
        market = '1'

    if(sector == None):
        sectorList = koapy.getSectorInfoAsList('013', market)
    else:
        sectorList = koapy.getSectorInfoAsList(sector, market)

    return sectorList


# 섹터 별 주가정보 서버로 전송
def sendStockInfo(sectorList: list):

    if isinstance(sectorList, list):
        res = []
        for sector in sectorList:
            print('[request datas]')
            print(sector)
            res.append(req.postStocks(sector))
            time.sleep(0.1)
        return res
    else:
        return None


# get parameters
def getParams():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hm:s:', [
                                   'market=', 'sector='])
    except getopt.GetoptError:
        print('main.py -m <market code> -s <sector code>')
        sys.exit(2)
    market = None
    sector = None

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -m <market code> -s <sector code>')
            sys.exit()
        elif opt in ('-m', '--market'):
            market = arg
        elif opt in ('-s', '--sector'):
            sector = arg
    if market:
        print('[input market code]: ', market)
    else:
        print('main.py -m <market code> -s <sector code>')
        sys.exit()

    if sector:
        print('[input sector code]:', sector)
    else:
        print('main.py -m <market code> -s <sector code>')
        sys.exit()

    return market, sector


# start main code
if __name__ == "__main__":
    market, sector = getParams()

    # define global variable req
    req = Client()
    print('[success connected lumen server]')

    # define global variable Koapy
    koapy = KoapyWrapper()

    # market={0:코스피}}, sector={013:전자기기}:
    response = main(str(market), str(sector))

    print(response)
