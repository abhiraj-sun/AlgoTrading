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
tgtPer = 1.5
slPer = 0.75
minPrice = 100


def getTargetAndStopLoss(ltp, isBuy):
    if isBuy:
        tarPrice = ltp + ((ltp * tgtPer) / 100)
        slPrice = ltp - ((ltp * slPer) / 100)
    else:
        tarPrice = ltp - ((ltp * tgtPer) / 100)
        slPrice = ltp + ((ltp * slPer) / 100)

    return round(tarPrice, 1), round(slPrice, 1)


def placeIntraDayOrder(isBuy, tradingSymbol, symbolToken, ltpPrice, qty):
    print(tradingSymbol)
    try:
        tarPrice, slTriggerPrice = getTargetAndStopLoss(ltpPrice, isBuy)
        slPrice = round((slTriggerPrice - 0.051 if isBuy else slTriggerPrice + 0.051), 2)

        slOrderParam = {
            "variety": "STOPLOSS",
            "tradingsymbol": tradingSymbol,
            "symboltoken": symbolToken,
            "transactiontype": 'SELL' if isBuy else 'BUY',
            "exchange": "NSE",
            "ordertype": "STOPLOSS_LIMIT",  ## STOPLOSS_MARKET
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": slPrice,
            "triggerprice": slTriggerPrice,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
        }

        tOrderParam = {
            "variety": "NORMAL",
            "tradingsymbol": tradingSymbol,
            "symboltoken": symbolToken,
            "transactiontype": 'SELL' if isBuy else 'BUY',
            "exchange": "NSE",
            "ordertype": "LIMIT",  ## STOPLOSS_MARKET
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": tarPrice,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
        }

        obj.placeOrder(slOrderParam)
        obj.placeOrder(tOrderParam)

        print(ltpPrice, tarPrice, slPrice, slTriggerPrice, qty)
    except Exception as e:
        print(e)


def setTargetAndStopLoss():
    orderData = obj.position()
    for pos in orderData['data']:
        netQty = int(pos['netqty'])
        if netQty != 0:
            isBuy = True if int(pos['buyqty']) > 0 else False
            th = threading.Thread(target=placeIntraDayOrder, args=(
            isBuy, pos['tradingsymbol'], pos['symboltoken'], float(pos['netprice']),  abs(int(pos['netqty']))))
            th.start()
            th.join()


setTargetAndStopLoss()
