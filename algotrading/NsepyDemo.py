import yfinance as yf
import pandas as pd
import json
import datetime as dt

start = dt.datetime(2021, 1, 1).date()
end = dt.datetime(2021, 10, 29).date()

basePercentageAsTimeFrame = {
    '15m': 0.4,
    '90m': 0.8,
    '1d': 1.4,
    '1wk': 2.8,
}
candleTimeFrame = '1wk'


def historicalData():
    try:
        cData = {}
        cData = yf.download(['TATAMOTORS.NS'], start, end, interval=candleTimeFrame, rounding=True)
        return cData
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


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


# get highest body and lowest week from all base candles
def getDemandZoneDistalAndProximalPoints(index, lastIndex, includeLast):
    high = 0
    low = candles.iloc[index + 1]['Low']  # low point
    for i in range(index + 1, lastIndex):
        # get high of Body
        h = candles.iloc[i]['Close'] if candles.iloc[i]['Type'] >= 1 else candles.iloc[i]['Open']

        high = h if h > high else high
        low = candles.iloc[i]['Low'] if candles.iloc[i]['Low'] < low else low

    if includeLast:
        low = candles.iloc[lastIndex]['Low'] if candles.iloc[lastIndex]['Low'] < low else low

    isValidZone = high < (candles.iloc[index]['Close'] + candles.iloc[index]['Open']) / 2

    return high, low, isValidZone


def findDemandZone(index):
    isContainBase = False
    isContainLegOut = False
    isDemandZone = False
    noOfBase = 0
    lastIndex = index
    high = 0
    low = 0

    for i in range(index + 1, index + 7):
        if i >= len(candles):
            break

        if candles.iloc[i]['Type'] > 1 or candles.iloc[i]['Type'] < -1:
            isContainLegOut = True
            lastIndex = i
            break
        else:
            isContainBase = True
            noOfBase += 1

    if isContainLegOut:
        if isContainBase:
            high, low, isDemandZone = getDemandZoneDistalAndProximalPoints(index, lastIndex,
                                                                           candles.iloc[lastIndex]['Type'] < 0)
        else:
            if candles.iloc[index]['Type'] > 2 and candles.iloc[lastIndex]['Type'] < -2:
                isDemandZone = True
                high = candles.iloc[index]['Open'] if candles.iloc[index]['Open'] > candles.iloc[lastIndex]['Close'] else candles.iloc[lastIndex]['Close']
                low = candles.iloc[index]['Low'] if candles.iloc[index]['Low'] < candles.iloc[lastIndex]['Low'] else candles.iloc[lastIndex]['Low']

    return lastIndex, noOfBase, high, low, isDemandZone


def printDemandZone():
    for index in range(len(candles)):
        if candles.iloc[index]['Type'] > 1:
            lastIndex, noOfBase, high, low, isDemandZone = findDemandZone(index)
            if isDemandZone:
                print(noOfBase, high, low)


candles = historicalData()
getCandleType()
candles = candles.iloc[::-1]
printDemandZone()
