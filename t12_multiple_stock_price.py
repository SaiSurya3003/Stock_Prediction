import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz  # Python Time Zone

def get_stock_data(symbol, date):
    stock = yf.Ticker(symbol)
    tz = pytz.timezone('America/New_York')
    start_date = tz.localize(datetime.strptime(date, '%y-%m-%d'))
    history = stock.history(start=start_date, end=start_date+timedelta(days=1))

    if not history.empty:
        last_row = history.iloc[-1]
        return {
            'Symbol': symbol,
            'Open': round(last_row['Open'], 2),
            'Close': round(last_row['Close'], 2),
            'High': round(last_row['High'], 2),
            'Low': round(last_row['Low'], 2)
        }
    else:
        return {'Symbol': 'N/A', 'Open': 'N/A', 'Close': 'N/A', 'High': 'N/A', 'Low': 'N/A'}

def last_5_bus_days():
    today = datetime.today().date()
    last_5_days = [today - timedelta(days=x) for x in range(1,8)] # For 5 Business days that may include Weekends, Count =7
    business_days = [day for day in last_5_days if day.weekday() < 5][:5] #{day.weekday() ---> 0: Monday, ..., 6: Sunday}
    return business_days

st.title("Stock Dashboard")

dates = last_5_bus_days()
date_strings = [date.strftime('%y-%m-%d') for date in dates]
selected_date = st.selectbox("Select Date", date_strings)

stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
stocks_data = []
for stock in stocks:
    stock_data = get_stock_data(stock, selected_date)
    stocks_data.append(stock_data)

df = pd.DataFrame(stocks_data)
st.write(f"Stock Data of Stocks for {selected_date}")
st.dataframe(df)