import yfinance as yf
import pandas as pd
import json
import datetime as dt

periodRange = "1y"

basePercentageAsTimeFrame = {
    '90m': 0.8,
    '1d': 1.4,
    '1wk': 2.8,
}
candleTimeFrame = '1d'


def historicalData():
    try:
        cData = {}
        cData = yf.download(['TATAMOTORS.NS'], period=periodRange, interval=candleTimeFrame, rounding=True)
        return cData
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


# ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', "Type"]
def isPositiveCandle(candle):
    if candle['Open'] < candle['Close']:
        return True
    else:
        return False


def getValueFromPercentage(openValue, per):
    return openValue * per / 100


def getPercentageFromValue(openValue, val):
    return val * 100 / openValue


def getCandlePercentage(isPositive, candle):
    if isPositive:
        diff = candle['Close'] - candle['Open']
    else:
        diff = candle['Open'] - candle['Close']
    return (diff * 100) / candle['Open']


def getCandleType():
    per = basePercentageAsTimeFrame[candleTimeFrame]
    typeArr = []
    for index in range(len(candles)):
        candle = candles.iloc[index]
        isPositive = isPositiveCandle(candle)
        candlePer = getCandlePercentage(isPositive, candle)
        if isPositive:
            if per * 5 < candlePer:
                cType = 4
            elif per * 3 < candlePer:
                cType = 3
            elif per < candlePer:
                if ((candle['High'] - candle['Close']) - (candle['Close'] - candle['Open'])) <= (
                        (candle['Close'] - candle['Open']) * 1.5):
                    cType = 2
                else:
                    cType = 1
            else:
                cType = 1
        else:
            if per * 5 < candlePer:
                cType = -4
            elif per * 3 < candlePer:
                cType = -3
            elif per < candlePer:
                if ((candle['High'] - candle['Close']) - (candle['Open'] - candle['Close'])) <= (
                        (candle['Open'] - candle['Close']) * 1.5):
                    cType = -2
                else:
                    cType = -1
            else:
                cType = -1
        typeArr.append(cType)
    candles["Type"] = typeArr


candles = historicalData()
getCandleType()
candles = candles.iloc[::-1]
print(candles)
