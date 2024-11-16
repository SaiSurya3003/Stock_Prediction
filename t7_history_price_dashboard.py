import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

ticker = "AAPL"
stock_data = yf.Ticker(ticker)
historical_data = stock_data.history(period="1y")

st.title(f"Historical data for {ticker}")
st.line_chart(historical_data['Close']) ## CLOSE is used to get the Daily Closed price of the Ticker for 1 year

st.write("Stock Price Chart")
fig, ax = plt.subplots()
ax.plot(historical_data.index, historical_data["Close"], label="CLOSE_PRICE")
ax.set_xlabel("DATE")
ax.set_ylabel("PRICE in $")
ax.set_title(f"{ticker} Stock Closure price over last 1 Year")
ax.legend()
st.pyplot(fig)