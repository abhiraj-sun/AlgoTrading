import datetime as dt
import yfinance as yf
import pandas as pd

tickers = ['TATAMOTORS.NS', 'INFY.NS','LT.NS']
start = dt.datetime.today() - dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame()

for ticker in tickers:
    cl_price[ticker] = yf.download(ticker, start, end)['Close']

# print(cl_price.describe())
# print(cl_price.tail())
daily_return = cl_price.pct_change()
print(daily_return.mean())
print(daily_return.std())
