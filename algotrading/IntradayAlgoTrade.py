from smartapi import SmartConnect
import pandas as pd
import json
from datetime import datetime

apiKey = "JCS10JLA"
clientID = "A380792"
password = "Yamaharx@47"

obj = SmartConnect(api_key=apiKey)
data = obj.generateSession(clientID, password)
tgtPer = 0.4
slPer = 0.2
tradingSymbol = "BANKBARODA-EQ"
symbolToken = "4668"
qty = 5


def getTargetAndStopLoss(ltp, isBuy):
    tarPrice = 0
    slPrice = 0
    slTriggerPrice = 0

    if isBuy:
        tarPrice = ltp + ((ltp * tgtPer) / 100)
        slPrice = ltp - ((ltp * slPer) / 100)
    else:
        tarPrice = ltp - ((ltp * tgtPer) / 100)
        slPrice = ltp + ((ltp * slPer) / 100)

    return round(tarPrice, 1), round(slPrice, 1)


def placeIntraDayOrder(isBuy):
    try:
        ltpData = obj.ltpData("NSE", tradingSymbol, symbolToken)
        # print(ltpData)
        ltpPrice = ltpData['data']['ltp']
        tarPrice, slPrice = getTargetAndStopLoss(ltpPrice, isBuy)
        slTriggerPrice = round((slPrice + 0.051 if isBuy else slPrice - 0.051), 2)
        print(ltpPrice, tarPrice, slPrice, slTriggerPrice)

        orderParam = {
            "variety": "NORMAL",
            "tradingsymbol": tradingSymbol,
            "symboltoken": symbolToken,
            "transactiontype": 'BUY' if isBuy else 'SELL',
            "exchange": "NSE",
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltpPrice,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
        }


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

        # obj.placeOrder(orderParam)
        # obj.placeOrder(slOrderParam)
        # obj.placeOrder(tOrderParam)

        return ltpPrice, tarPrice, slPrice, slTriggerPrice
    except Exception as e:
        print(e)


print(placeIntraDayOrder(True))
