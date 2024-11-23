import yfinance as yf

stock_data_file = 'stockData.txt'
outcome_file = "stockDataOutcome.txt"
with open(outcome_file, "w") as output_file:
    output_file.write(f"{'Stock Name':<20}{'Previous Close':<20}{'Market Open':<20}{'Daily High':<20}{'Daily Low':<20}\n")

    with open(stock_data_file, 'r') as file:
        stock_names = file.read().splitlines()

    for symbol in stock_names:
        stock_data = yf.Ticker(symbol)
        info = stock_data.info
        try:
            previous_close = info.get('regularMarketPreviousClose', 'N/A')
            market_open = info.get('regularMarketOpen', 'N/A')
            day_high = info.get('regularMarketDayHigh', 'N/A')
            day_low = info.get('regularMarketDayLow', 'N/A')
            output_file.write(f"{symbol:<20}{previous_close:<20}{market_open:<20}{day_high:<20}{day_low:<20}\n")
        except KeyError:
            output_file.write(f"No Data available for {symbol}\n")