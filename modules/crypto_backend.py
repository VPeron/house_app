import pandas_datareader as web
import datetime as dt
import streamlit as st


@st.cache
def get_currency_data(currency, start):
    crypto_symbols = {
    'Bitcoin':'BTC-USD',
    'Ethereum':'ETH-USD',
    'Monero':'XMR-USD'
    }
    end = dt.datetime.now()
    currency = web.DataReader(crypto_symbols[currency], 'yahoo', start, end)
    return currency
 