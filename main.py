from modules.koapy.koapywrapper import KoapyWrapper
from modules.client.client import Client
import json
import time
# main func
def main(market: str,sector=None):
    sectors = getSectors(market)
    results = []
    sectorDict = {}

    if(sector):
        sectorDict['code'] = sector
        sectorDict['name'] = sectors['sectors_raw'][sector]
        sectorDict['data'] = getStockInfoBySector(market, sector)
        results.append(sectorDict)
    else:
        for s in sectors['sectors']:
            sectorDict['code'] = s['code']
            sectorDict['name'] = s['name']
            sectorDict['data'] = getStockInfoBySector(market, s['code'])
            results.append(sectorDict)

    return sendStockInfo(results)   
# 섹터 정보 가져오기 
def getSectors(market: str):
    sectors = req.getSectors(market)
    
    return sectors

# 섹터 별 주가정보           
def getStockInfoBySector(market: str,sector: str):
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

# 섹터 별 주가정보 서버로 전송
def sendStockInfo(sectorList: list):
    
    if isinstance(sectorList,list):
        res = []
        for sector in sectorList:
            print('[request datas]')
            print(sector)
            res.append(req.postStocks(sector))
            time.sleep(0.1)
        return res
    else:
        return None
    
# define global variables
req = Client()
print('[success connected lumen server]')

koapy = KoapyWrapper()

# start main code
if __name__ == "__main__":
    # market={0:코스피}}, sector={013:전자기기}:
    response = main('kospi','013')

    print(response)
    