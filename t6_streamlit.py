import yfinance as yf
import streamlit as st

ticker = "AAPL"

stock_data = yf.Ticker(ticker)

st.title("Stock Information for AAPL")

st.write("Company Information") ## writing the information we want to display on the page
st.write(stock_data.info) ## Writing the acquired information abou the company

st.write("Earning Calender")
st.write(stock_data.earnings)

## Run the file in Powershell using streamlit run .\(FILENAME)