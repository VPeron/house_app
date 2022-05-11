import streamlit as st
import pandas as pd
from gsheetsdb import connect
import matplotlib.pyplot as plt
import seaborn as sns


COMD_SHEET_URL = st.secrets["comd_sheet"]


@st.cache(ttl=600)
def run_query(query):
    conn = connect()
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def get_comd_data():
    rows = run_query(f'SELECT * FROM "{COMD_SHEET_URL}"')
    data = pd.DataFrame(rows)
    return data


def pre_proc_data(df):
    df = df[df['Amount'] < 0]
    df = df.copy()
    df['Amount'] = abs(df['Amount'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def plot_monthly_data(df_month, select_month, select_year):
    df_month = df_month.reset_index()
    df_month.columns = ['Labels', 'Amount']

    fig, ax = plt.subplots(figsize=(15,5))
    sns.barplot(x='Labels', y='Amount', data=df_month)
    ax.tick_params(axis='x', rotation=60)
    plt.title(f"{select_month} {select_year}")
    plt.ylabel('Amount €')
    plt.xlabel('Labels')
    ax.grid()
    st.pyplot(fig)