import yfinance as yf

ticker = 'AAPL'
stock_data = yf.Ticker(ticker)

stock_history = stock_data.history(period='1mo')

print(stock_history)