import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import joblib
import os
from datetime import datetime, time, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error #For providing the prediction values
from tensorflow.keras.models import load_model #For Neural networks, pretrained Keras models

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(base_dir, 'sp500_stocks.csv')
sp500_stocks = pd.read_csv(csv_file_path)

def calculate_moving_avg(data, window_size):
    return data.rolling(window=window_size).mean()

def create_dataset(data, look_back=100):
    X,Y = [],[] # X,Y -> input{prev 100 days}, output{stock price of 101st day}
    for i in range(len(data)-look_back):
        X.append(data[i:(i + look_back)])
        Y.append(data[i + look_back])
    return np.array(X), np.array(Y)

def main():
    st.sidebar.title("Stock Forecast")
    st.sidebar.markdown("Select Stock and Date range")
    stock_symbol = st.sidebar.selectbox("Select Ticker", sp500_stocks['Symbol'])
    start_date = st.sidebar.date_input("Select Start Date", datetime.now()-timedelta(days=365))
    end_date = st.sidebar.date_input("Select End Date", datetime.now())
    selected_model = st.sidebar.radio(("Select Model", ("Neural Network", "Random Forest", "Linear Regression")))
    if stock_symbol:
        try:
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            st.subheader(f"Stock Data for {stock_symbol}")
            st.write(stock_data.head(50))
            st.write("...")

            stock_data["MA100"] = calculate_moving_avg(stock_data['Close'], 100)
            stock_data["MA200"] = calculate_moving_avg(stock_data['Close'], 200)

            st.header("Price vs MA100")
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
            fig1.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA100'], mode='lines', name='MA100'))
            st.plotly_chart(fig1)

            st.header("Price vs MA100 and MA200")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA100'], mode='lines', name='MA100'))
            fig2.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA200'], mode='lines', name='MA200'))
            st.plotly_chart(fig2)

            candlestick = go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         close=stock_data['Close'],
                                         high=stock_data['high'],
                                         low=stock_data['Low'],
                                         name='Candle Stick')
            candlestick_layout = go.Layout(title='Candle Stick Chart')
            candlestick_fig = go.Figure(data=candlestick, layout=candlestick_layout)
            st.plotly_chart(candlestick_fig)

            volume_fig = go.Figure()
            volume_fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Trade Volume'))
            volume_fig.update_layout(title="Volume Plot")
            st.plotly_chart(volume_fig)