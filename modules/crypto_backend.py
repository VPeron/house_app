import pandas as pd
import pandas_datareader as web
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def get_start_end():
    start = dt.datetime(2018,1,1)
    end = dt.datetime.now()
    return start, end


@st.cache()
def get_currency_data(currency):
    crypto_symbols = {
    'Bitcoin':'BTC-USD',
    'Ethereum':'ETH-USD',
    'Monero':'XMR-USD'
    }
    start, end = get_start_end()
    currency = web.DataReader(crypto_symbols[currency], 'yahoo', start, end)
    return currency


def monitor_ranges():
    st.header('Monitoring Ranges')
    coin_range_alert = {
        'Bitcoin': {'Min':35000, 'Max':45000},
        'Ethereum':{'Min':2500, 'Max':3500},
        'Monero':{'Min':200, 'Max':300},
    }
    st.table(coin_range_alert)
    crypto_info = {}
    crypto_data = {}
    for coin in coin_range_alert.keys():
        data = get_currency_data(coin)
        crypto_data[coin] = data
        crypto_info[coin] = {
            'min':data['Close'].min(), 
            'max':data['Close'].max(), 
            'mean':data['Close'].mean(),
            'current':data['Close'][-1],
            'shift':data['Close'][-1] - data['Close'][-2]
            }
        if crypto_info[coin]['current'] <= coin_range_alert[coin]['Min'] or crypto_info[coin]['current'] >= coin_range_alert[coin]['Max']:
            st.error(f"{coin} is out of range at {round(crypto_info[coin]['current'],2)}")
        else:
            st.success(f"{coin} is within range at {round(crypto_info[coin]['current'],2)}")

    st.header('Historical Data Summary (Close)')
    st.table(crypto_info)
    return crypto_data


def plot_data(crypto_data):
    start, end = get_start_end()
    coin_menu = st.selectbox('Select a coin', crypto_data.keys())
    if coin_menu:
        state_menu = st.selectbox('Select a view', ['Open', 'Close', 'Low', 'High', 'Volume'])
        if state_menu:
            df = pd.DataFrame(crypto_data[coin_menu][state_menu])
            st.title(f"{coin_menu} - Historical line plot")
            fig, ax = plt.subplots(figsize=(15,8))
            plt.title(f'{str(start)[:10]} until {str(end)[:10]} {coin_menu} - {state_menu}')
            sns.lineplot(x=df.index, y=df[state_menu], data=df)
            plt.grid()
            st.pyplot(fig)
 