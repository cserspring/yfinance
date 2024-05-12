import yfinance as yf
import sys
from datetime import datetime, timedelta

class DataPoint:
    def __init__(self, t, p):
        self.t = t
        self.p = p

    def __str__(self):
        return f"{self.t}: {self.p:.2%}"

startDate = sys.argv[1]
endDate = sys.argv[2]

format = "%Y-%m-%d"
# For some input days, they're not trading days, so we need to read
# one week's data and get the day which is close to the input day
d00 = datetime.strptime(startDate, format) - timedelta(days=7)
d01 = datetime.strptime(startDate, format)
d10 = datetime.strptime(endDate, format) - timedelta(days=7)
d11 = datetime.strptime(endDate, format)

tickers = [sys.argv[3]] if len(sys.argv) >= 4  else ["MSFT"]
res = []
for ticker in tickers:
    t = yf.Ticker(ticker)
    try:
        h0 = t.history(start=d00, end=d01)
        h1 = t.history(start=d10, end=d11)
        now = h1["Close"].iloc[-1] # The result is in ascending order by date
        prev = h0["Close"].iloc[-1]
        p = (now - prev) / prev
        res.append(DataPoint(ticker.upper(), p))
    except Exception as e:
        pass
res.sort(key=lambda x:x.p, reverse=True)
print(*res, sep="\n")
