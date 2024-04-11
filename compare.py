import yfinance as yf
import sys
import csv
from datetime import datetime, timedelta, date

class DataPoint:
    def __init__(self, t, p):
        self.t = t
        self.p = p

    def __str__(self):
        return f"{self.t}: {self.p:.2%}"

csvFile = sys.argv[1]
ticker = sys.argv[2]
cache = {}
yahooFormat = "%Y%m%d"
totalCurValue = 0.0
originalValue = 0.0
totalShares = 0.0
format = "%Y-%m-%d"
todayStart = datetime.strptime(str(date.today()), format) - timedelta(days=7)
todayEnd = datetime.strptime(str(date.today()), format) + timedelta(days=1)
t = yf.Ticker(ticker)
with open(csvFile, mode='r') as file:
    lines = csv.DictReader(file)
    for line in lines:
        buyValue = float(line['Purchase Price']) * float(line['Quantity'])
        originalValue += buyValue
        originalStart = datetime.strptime(line['Trade Date'], yahooFormat)
        originalEnd = datetime.strptime(line['Trade Date'], yahooFormat) + timedelta(days=1)

        if line['Symbol'] in cache:
            curPrice = cache[line['Symbol']]
        else:
            s = yf.Ticker(line['Symbol'])
            curPrice = float((s.history(start=todayStart, end=todayEnd)['Close'])[-1])
            cache[line['Symbol']] = curPrice
        totalCurValue += curPrice * float(line['Quantity'])

        shares = buyValue / float((t.history(start=originalStart,end=originalEnd)['Close'])[-1])
        totalShares += shares


h0 = t.history(start=todayStart, end=todayEnd)
t_price_today = h0['Close'][-1]
totalTickerValue = totalShares * t_price_today

print(f"Deposit: {originalValue}")
print(f"Current value: {totalCurValue}")
print(f"Invested in {ticker}: {totalTickerValue}")
print(f"Current gain: {(totalCurValue - originalValue)/originalValue :.2%}")
print(f"Ticker gain: {(totalTickerValue - originalValue)/originalValue :.2%}")
