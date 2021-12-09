from smartapi import SmartConnect
import pandas as pd
import json
from datetime import datetime

apiKey = "JCS10JLA"
clientID = "A380792"
password = "Yamaharx@47"

obj = SmartConnect(api_key=apiKey)
basePercentageAsTimeFrame = {
    'FIFTEEN_MINUTE': 0.4,
    'ONE_HOUR': 0.8,
    'ONE_DAY': 1.4,
}
candleTimeFrame = 'ONE_HOUR'

data = obj.generateSession(clientID, password)


#
# refreshToken = data['data']['refreshToken']
# feedToken = obj.getfeedToken()
#
# userProfile = obj.getProfile(refreshToken)


def historicalData():
    try:
        historicParam = {
            "exchange": "NSE",
            "symboltoken": "3456",
            "interval": candleTimeFrame,
            "fromdate": "2021-09-13 09:00",
            "todate": "2021-10-14 16:30"
        }
        hisData = obj.getCandleData(historicParam)
        cData = hisData['data']
        cData.reverse()
        return cData
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


# ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', "Type"]
def isPositiveCandle(candle):
    if candle[1] < candle[4]:
        return True
    else:
        return False


def getValueFromPercentage(openValue, per):
    return openValue * per / 100


def getPercentageFromValue(openValue, val):
    return val * 100 / openValue


'''
def getCandleType():
    for index, candle in enumerate(candles):
        if isPositiveCandle(candle):
            if ((candle[2] - candle[3]) - (candle[4] - candle[1])) < (candle[4] - candle[1]):
                candles[index].append(2)
            else:
                candles[index].append(1)
        else:
            # 2.4 -
            if ((candle[2] - candle[3]) - (candle[1] - candle[4])) > (candle[1] - candle[4]):
                candles[index].append(-1)
            else:
                candles[index].append(-2)
'''


def getCandlePercentage(isPositive, candle):
    if isPositive:
        diff = candle[4] - candle[1]
    else:
        diff = candle[1] - candle[4]
    return (diff * 100) / candle[1]


def getCandleType():
    per = basePercentageAsTimeFrame[candleTimeFrame]
    for index, candle in enumerate(candles):
        isPositive = isPositiveCandle(candle)
        candlePer = getCandlePercentage(isPositive, candle)
        if isPositive:
            if per * 5 < candlePer:
                candles[index].append(4)
            elif per * 3 < candlePer:
                candles[index].append(3)
            elif per < candlePer:
                if ((candle[2] - candle[3]) - (candle[4] - candle[1])) <= ((candle[4] - candle[1]) * 1.5):
                    candles[index].append(2)
                else:
                    candles[index].append(1)
            else:
                candles[index].append(1)
        else:
            if per * 5 < candlePer:
                candles[index].append(-4)
            elif per * 3 < candlePer:
                candles[index].append(-3)
            elif per < candlePer:
                if ((candle[2] - candle[3]) - (candle[1] - candle[4])) <= ((candle[1] - candle[4]) * 1.5):
                    candles[index].append(-2)
                else:
                    candles[index].append(-1)
            else:
                candles[index].append(-1)


# get highest body and lowest week from all base candles
def getDemandZoneDistalAndProximalPoints(index, lastIndex, includeLast):
    high = 0
    low = candles[index + 1][3]  # low point
    isValidZone = False
    for i in range(index + 1, lastIndex):
        # get high of Body
        h = candles[i][4] if candles[i][6] >= 1 else candles[i][1]

        high = h if h > high else high
        low = candles[i][3] if candles[i][3] < low else low

    if includeLast:
        low = candles[lastIndex][3] if candles[lastIndex][3] < low else low

    isValidZone = high < (candles[index][4] + candles[index][1]) / 2

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

        if candles[i][6] > 1 or candles[i][6] < -1:
            isContainLegOut = True
            lastIndex = i
            break
        else:
            isContainBase = True
            noOfBase += 1

    if isContainLegOut:
        if isContainBase:
            high, low, isDemandZone = getDemandZoneDistalAndProximalPoints(index, lastIndex,
                                                                           candles[lastIndex][6] < 0)
        else:
            if candles[index][6] > 2 and candles[lastIndex][6] < -2:
                isDemandZone = True
                high = candles[index][1] if candles[index][1] > candles[lastIndex][4] else candles[lastIndex][4]
                low = candles[index][3] if candles[index][3] < candles[lastIndex][3] else candles[lastIndex][3]

    return lastIndex, noOfBase, high, low, isDemandZone


candles = historicalData()
# print(candles)
getCandleType()


def printDemandZone():
    for index in range(len(candles)):
        if candles[index][6] > 1:
            lastIndex, noOfBase, high, low, isDemandZone = findDemandZone(index)
            if isDemandZone:
                print(candles[index], noOfBase, high, low)


printDemandZone()


def printData():
    columns = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', "Type"]

    df = pd.DataFrame(candles, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S')
    print(df)
