import yfinance as yf
import streamlit as st

ticker = "AAPL"
stock_data = yf.Ticker(ticker)

balance_sheet = stock_data.balance_sheet
income_statement = stock_data.financials
cash_flow = stock_data.cash_flow

st.title(f"Financial information about {ticker} Stock")

st.write("Balance Sheet")
st.write(balance_sheet)

st.write("Income Statement")
st.write(income_statement)

st.write("Cash Flow")
st.write(cash_flow)
