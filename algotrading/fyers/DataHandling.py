from fyers_api import fyersModel
from fyers_api import accessToken
import threading

client_id = "8LODKCYPOR-100"  # "XA02959"
secret_key = "W32UU7RTE4"
redirect_uri = "http://127.0.0.1:5000/login"

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2NDA0MTEzMTQsImV4cCI6MTY0MDQ3ODYzNCwibmJmIjoxNjQwNDExMzE0LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaHhyQ3kyVHM1RXFHY2xUTTE4WG84ZGU1TjhBWURabUJFbzA1ekdMWDZzRElINlhqUktnSm1jUGUwYkN1Q2pVaDRjNXV3UnBobUZiWUlTT0l4YmlsQUZJZWRUN1d6eXFWa0NSbUVqZzlzOEI3NUh2OD0iLCJkaXNwbGF5X25hbWUiOiJBQkhJSkVFVFNJTkdIIFBSRU1TSU5HSCBSIiwiZnlfaWQiOiJYQTAyOTU5IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.XD_DHA32s9UmctCN2j6sG1XUDDcHRUiHBi2riZNW0nM'

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)

tgtPer = 2
slPer = 1
minPrice = 4000


def getTargetAndStopLoss(ltp):
    tarPrice = ((ltp * tgtPer) / 100)
    slPrice = ((ltp * slPer) / 100)
    return round(tarPrice, 1), round(slPrice, 1)


def getQuantity(ltp):
    qty = (minPrice * 5) / ltp
    return round(qty, 0)


def placeBracketOrder(symbol, qty, isBuy, stopLoss, takeProfit):
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": 2,
        "side": 1 if isBuy else -1,
        "productType": "BO",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "stopLoss": stopLoss,
        "offlineOrder": "False",
        "takeProfit": takeProfit
    }
    print(fyers.place_order(data))


def placeNormalIntradayOrder(symbol, qty, isBuy, stopLoss, takeProfit):
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": 2,
        "side": 1 if isBuy else -1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "stopLoss": 0,
        "offlineOrder": "False",
        "takeProfit": 0
    }


def placeIntraDayOrder(isBuy, tradingSymbol):
    try:
        symbol = "NSE:" + tradingSymbol + "-EQ"
        data = {"symbols": symbol}
        quote = fyers.quotes(data)
        ltpPrice = quote['d'][0]['v']['open_price']
        qty = getQuantity(ltpPrice)

        takeProfit, slTriggerPrice = getTargetAndStopLoss(ltpPrice)
        stopLoss = round((slTriggerPrice - 0.001 if isBuy else slTriggerPrice + 0.001), 2)

        # Place order
        placeBracketOrder(symbol, qty, isBuy, stopLoss, takeProfit)

        print(symbol, ltpPrice, takeProfit, stopLoss, slTriggerPrice, qty)
    except Exception as e:
        e


tradingSymbols = ["NMDC", "SAIL", "FEDERALBNK", "BHEL", "HFCL", "NETWORK18", "TV18BRDCST",
                  "IDFCFIRSTB", "BANKBARODA", "PNB", "CANBK", "IDFC", "ALEMBICLTD", "SBIN", "LUPIN"]
orderType = [False, False, False, False, False, False, True, False, False, True, False, False, False, False, False]


def placeIntraDayMultiOrders():
    length = len(tradingSymbols)
    for i in range(length):
        th = threading.Thread(target=placeIntraDayOrder, args=(orderType[i], tradingSymbols[i]))
        th.start()
        th.join()


placeIntraDayMultiOrders()
