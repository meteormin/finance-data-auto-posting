from modules.koapy.koapywrapper import KoapyWrapper
from modules.client.client import Client
import json
import time
import sys
import getopt


# main func


def getBySector(market: str, sector=None):
    sectors = getSectors()
    sendSectorList(sectors, market)
    results = []
    sectorDict = {}

    if sector:
        sectorName = None
        for s in sectors:
            if sector == s['code']:
                sectorName = s['name']

        sectorDict['code'] = sector
        sectorDict['name'] = sectorName
        sectorDict['data'] = getStockInfoBySector(market, sector)
        tempList = []
        for stock in sectorDict['data']:
            basic = getStockBasicInfo(stock['code'])
            tempList.append(basic)
            time.sleep(0.1)
        sectorDict['data'] = tempList
        results.append(sectorDict)

    else:
        for s in sectors:
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

    return sendStockInfo('sector', results)


# 섹터 정보 가져오기
def getSectors():
    # sectors = req.getSectors(market)
    sectors = koapy.getSectorList()
    return sectors


def sendSectorList(results, market):
    print('[request datas]')
    print(results)

    res = req.postSectorList({'data': results}, market)

    print('[response data]')
    print(res)
    return res


# 섹터 별 주가정보
def getStockInfoBySector(market: str, sector: str):
    sectorList = []

    if market == 'kospi':
        market = '0'
    elif market == 'kosdaq':
        market = '1'

    if (sector == None):
        sectorList = koapy.getStockInfoBySectorAsList('013', market)
    else:
        sectorList = koapy.getStockInfoBySectorAsList(sector, market)

    return sectorList


def getStockBasicInfo(code: str):
    return koapy.getStockBasicInfoAsDict(code)


def getSectorInfo(market: str, sector: str):
    sectorInfo = []

    if market == 'kospi':
        market = '0'
    elif market == 'kosdaq':
        market = '1'

    if sector is None:
        sectorList = koapy.getSectorInfoAsList('013', market)
    else:
        sectorList = koapy.getSectorInfoAsList(sector, market)

    return sectorList


# 섹터 별 주가정보 서버로 전송
def sendStockInfo(method, reqList: list):
    if isinstance(reqList, list):
        res = []
        for r in reqList:
            print('[request datas]')
            print(r)
            res.append(req.postStocks(method, r))
            time.sleep(0.1)
        print('[response data]')
        print(res)
        return res
    else:
        return None


def sendThemeList(results):
    print('[request datas]')
    print(results)

    res = req.postThemeList({'data': results})

    print('[response data]')
    print(res)
    return res


def getByThemeList():
    return koapy.getThemeGroupListAsDict()


def getByTheme(theme):
    themes = getByThemeList()
    sendThemeList(themes)

    tempList = []
    results = []
    themeDict = {}

    if theme == 'all':
        for value in themes:
            stockCodes = koapy.getThemeGroupCodeAsList(str(value['code']))
            for code in stockCodes:
                basic = getStockBasicInfo(code)
                tempList.append(basic)
                time.sleep(0.1)
            themeDict['code'] = value['code']
            themeDict['name'] = value['name']
            themeDict['data'] = tempList
            results.append(themeDict)
    else:
        for value in themes:
            if value['code'] == theme:
                code = value['code']
                name = value['name']
        themeDict['code'] = code
        themeDict['name'] = name
        stockCodes = koapy.getThemeGroupCodeAsList(str(theme))
        for code in stockCodes:
            basic = getStockBasicInfo(code)
            tempList.append(basic)
            time.sleep(0.1)
        themeDict['data'] = tempList
        results.append(themeDict)

    return sendStockInfo('theme', results)


# get parameters


def getParams():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hm:s:t:', [
            'market=', 'sector=', 'theme='])
    except getopt.GetoptError:
        print('main.py -m <market code> -s <sector code>')
        sys.exit(2)
    market = None
    sector = None
    theme = None
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -m <market code> -s <sector code> | -t <theme code>')
            sys.exit()
        elif opt in ('-m', '--market'):
            market = arg
        elif opt in ('-s', '--sector'):
            sector = arg
        elif opt in ('-t', '--theme'):
            theme = arg
        else:
            print('main.py -m <market code> -s <sector code> | -t <theme code>')
            sys.exit()
    if theme:
        print('[input theme code]: ', theme)
        return {'theme': theme}
    else:
        if market:
            print('[input market code]: ', market)
        else:
            print('main.py -m <market code> -s <sector code> | -t <theme code>')
            sys.exit()

        if sector:
            print('[input sector code]:', sector)
        else:
            print('main.py -m <market code> -s <sector code> | -t <theme code>')
            sys.exit()

    return {'market': market, 'sector': sector}


# start main code
if __name__ == "__main__":
    params = getParams()

    # define global variable req
    req = Client()
    print('[success connected lumen server]')

    # define global variable Koapy
    koapy = KoapyWrapper()

    if 'theme' in params:
        response = getByTheme(str(params['theme']))
    elif 'market' in params and 'sector' in params:
        # market={0:코스피}}, sector={013:전자기기}:
        response = getBySector(str(params['market']), str(params['sector']))

    print(response)
