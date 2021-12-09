#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 00:22:34 2021

@author: abhiraj
"""

import yfinance as yf
import pandas as pd
import json
import datetime as dt

tickers = ["TATAMOTORS.NS", "INFY.NS"]
periods = ['1y', '2y']
intervals = ['1d', '1wk']
basePercentageAsTimeFrame = {
    '90m': 0.8,
    '1d': 1.4,
    '1wk': 2.8
}

ticker_data = {}
ticker_avg = {}
zone_data = {}


def isPositiveCandle(candle):
    if candle['Open'] < candle['Close']:
        return True
    else:
        return False


def getValueFromPercentage(openValue, per):
    return openValue * per / 100


def getPercentageFromValue(openValue, val):
    return val * 100 / openValue


def getCandlePercentageForTicker(DF):
    candles = DF.copy()
    candles["per"] = ((candles["Open"].sub(candles["Close"]).abs() * 100) / candles["Open"])
    return candles.loc[:, ["per"]]


def getCandleType(intv, CANDLES):
    candles = CANDLES.copy()
    per = basePercentageAsTimeFrame[intv]
    typeArr = []
    for index in range(len(candles)):
        candle = candles.iloc[index]
        isPositive = isPositiveCandle(candle)
        if isPositive:
            if per * 5 < candle["Perc"]:
                cType = 4
            elif per * 3 < candle["Perc"]:
                cType = 3
            elif per < candle["Perc"]:
                if ((candle['High'] - candle['Close']) - (candle['Close'] - candle['Open'])) <= (
                        (candle['Close'] - candle['Open']) * 1.5):
                    cType = 2
                else:
                    cType = 1
            else:
                cType = 1
        else:
            if per * 5 < candle["Perc"]:
                cType = -4
            elif per * 3 < candle["Perc"]:
                cType = -3
            elif per < candle["Perc"]:
                if ((candle['High'] - candle['Close']) - (candle['Open'] - candle['Close'])) <= (
                        (candle['Open'] - candle['Close']) * 1.5):
                    cType = -2
                else:
                    cType = -1
            else:
                cType = -1
        typeArr.append(cType)
    return typeArr


def getTickerDataFromApiByTicker():
    for ticker in tickers:
        period_data = {}
        for i in range(len(intervals)):
            temp = yf.download(ticker, period=periods[i], interval=intervals[i])
            temp.dropna(how='any', inplace=True)
            period_data[intervals[i]] = temp
        ticker_data[ticker] = period_data


def addCandleTypeInTickerData():
    for ticker in tickers:
        for intv in intervals:
            ticker_data[ticker][intv][["Candle Per"]] = getCandlePercentageForTicker(ticker_data[ticker][intv])
            ticker_data[ticker][intv + "_avg"] = ticker_data[ticker][intv]["Candle Per"].max()
            # ticker_data[ticker][intv][["Type"]] = getCandleType(intv, ticker_data[ticker][intv])


getTickerDataFromApiByTicker()
addCandleTypeInTickerData()
