from smartapi import SmartConnect
import pandas as pd
import json
from datetime import datetime
import threading
import os

apiKey = "JCS10JLA"
clientID = "A380792"
password = "Yamaharx@47"

obj = SmartConnect(api_key=apiKey)
data = obj.generateSession(clientID, password)
tgtPer = 1
slPer = 0.5
minPrice = 150


def getQuantity(ltp):
    qty = (minPrice*5) / ltp
    return round(qty, 0)


def placeIntraDayOrder(isBuy, tradingSymbol, symbolToken):
    try:
        ltpData = obj.ltpData("NSE", tradingSymbol, symbolToken)
        print(ltpData)
        ltpPrice = ltpData['data']['ltp']
        qty = getQuantity(ltpPrice)

        orderParam = {
            "variety": "NORMAL",
            "tradingsymbol": tradingSymbol,
            "symboltoken": symbolToken,
            "transactiontype": 'BUY' if isBuy else 'SELL',
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": 0,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
        }
        obj.placeOrder(orderParam)

        print(ltpPrice, qty)
    except Exception as e:
        print(e)


tradingSymbols = ["NMDC-EQ", "SAIL-EQ", "FEDERALBNK-EQ", "BHEL-EQ", "HFCL-EQ", "NETWORK18-EQ", "TV18BRDCST-EQ",
                  "IDFCFIRSTB-EQ", "BANKBARODA-EQ", "PNB-EQ", "CANBK-EQ",
                  "IDFC-EQ", "ALEMBICLTD-EQ"]
symbolTokens = ["15332", "2963", "1023", "438", "21951", "14111", "14208", "11184", "4668", "10666", "10794", "11957",
                "79"]
orderType = [False, False, False, False, False, False, True, False, False, True, False, False, False]


def placeIntraDayMultiOrders():
    length = len(tradingSymbols)
    for i in range(length):
        th = threading.Thread(target=placeIntraDayOrder, args=(orderType[i], tradingSymbols[i], symbolTokens[i]))
        th.start()
        th.join()


placeIntraDayMultiOrders()
