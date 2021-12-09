import pandas as pd
import datetime as dt
import yfinance as yf

start = dt.datetime(2021, 10, 1).date()
end = dt.datetime(2021, 11, 3).date()

candleTimeFrame = '1d'


def historicalData():
    try:
        cData = yf.download(['TATAMOTORS.NS'], start, end, interval=candleTimeFrame, rounding=True)
        return cData
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


print(historicalData())
