from src.koapy.koapywrapper import KoapyWrapper

import json

# connect my lumen server
req = Client()

print('[success connected lumen server]')

# connect kiwoom api
# use Koapy
# I wrapped this package
koapy = KoapyWrapper()

sectors = req.getSectors()

for key,val in sector.items():
    if(key == 'kospi' OR key == 'kosdaq' OR key == 'kospi200'):
        marketCode = val['market_code']
        sectors = val['sectors']
        sectorList = koapy.getStockInfoBySectorAsList('013')
    else:
        break

# get sector list
# need define sector list... first, '013' is meanning '전자기기'
sectors



# send to my lumen server
req.postStocks({'sector':'013','data':sectorList})