import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "DIS"]

st.title("Top 10 Stock Analysis SMA50 and SMA200")

st.write("""
SMA = Simple Moving Average
50 Day SMA is Short Term Indicator
200 Day SMA is Long Term Indicator""")

for stock in stocks:
    stock_symbol = yf.Ticker(stock)
    history = stock_symbol.history(period="5y")

    history['SMA_50'] = history['Close'].rolling(window=50).mean()
    history['SMA_200'] = history['Close'].rolling(window=200).mean()

    fig, ax = plt.subplots(figsize=(14,7))
    ax.plot(history['Close'], label=f"{stock} Close", alpha=0.5)
    ax.plot(history['SMA_50'], label=f"{stock} SMA50", alpha=0.75)
    ax.plot(history['SMA_200'], label=f"{stock} SMA200", alpha=0.75)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"{stock_symbol} - Close Price and Moving Averages")

    st.pyplot(fig)

st.write("If 50 Day SMA is above 200 Day SMA - BULL or UPWARD. If below - BEAR or DOWNWARD")