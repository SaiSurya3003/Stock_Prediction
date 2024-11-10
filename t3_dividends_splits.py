import yfinance as yf

ticker = "AAPL"

stock_data = yf.Ticker(ticker)

dir(stock_data)

print(dir(stock_data))

print(stock_data.info)

print(stock_data.financials)

print(stock_data.recommendations)

print(stock_data.earnings)

print(stock_data.dividends)

print(stock_data.splits)

financial = stock_data.financials
html_file_path = f"{ticker}_financials.html"
financial.to_html(html_file_path)

print(f"Financial Information is saved to {html_file_path}")
