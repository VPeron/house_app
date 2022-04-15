# import pandas as pd
import pandas_datareader as web
import datetime as dt
# import matplotlib.pyplot as plt
# import seaborn as sns
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
    
# if __name__ == "__main__":
#     start = dt.datetime(2020,1,1)
#     end = dt.datetime.now()
#     coins = ['Bitcoin', 'Ethereum', 'Monero']
#     crypto_data = {}
#     for coin in coins:
#         data = get_currency_data(coin, start)
#         crypto_data[coin] = data
    
#     coin_menu = st.selectbox('Select a coin', crypto_data.keys())
#     if coin_menu:
#         state_menu = st.selectbox('Select a view', ['Open', 'Close', 'Low', 'High', 'Volume'])
#         if state_menu:
#             df = pd.DataFrame(crypto_data[coin_menu][state_menu])
#             # st.write(df)
#             st.title(f"{coin_menu}")
#             fig, ax = plt.subplots(figsize=(15,8))
#             plt.title(f'{str(start)[:10]} until {str(end)[:10]} {coin_menu} - {state_menu}')
#             sns.lineplot(x=df.index, y=df[state_menu], data=df)
#             plt.grid()
#             st.pyplot(fig)