import gspread
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



def get_comd_data():
    gc = gspread.service_account_from_dict(st.secrets['GCP_CREDENTIALS'])
    sh = gc.open("COMDIRECT_SHEET")
    #TODO: catch connection error here? TransportError
    worksheet = sh.sheet1
    list_of_lists = worksheet.get_all_values()
    data = pd.DataFrame(list_of_lists)
    data.columns = [i for i in data.T[0]]
    data.drop(0, axis=0, inplace=True)
    return data


def shorten_float(text):
    #annoying annotation from gsheets that i cant convert to float payments with more than four digits (above 1k).
    if len(text) > 6:
        text = text[:6]
    return text


def prepproc_feateng_data(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Amount'] = data['Amount'].apply(shorten_float)
    data['Amount'] = data['Amount'].astype({"Amount": float}, errors='raise')
    data['Month'] = data['Date'].dt.month_name()
    data['Year'] = data['Date'].dt.year
    return data


def data_split(df): 
    df_payments = df[df['Amount'] < 0]
    df_deposits = df[df['Amount'] > 0]
    df_deposits.drop('Labels', axis=1, inplace=True)
    return df_payments, df_deposits


def split_pay_year(df_payments):
    df_payments_2021 = df_payments[df_payments['Year'] == 2021]
    df_payments_2022 = df_payments[df_payments['Year'] == 2022]
    return df_payments_2021, df_payments_2022


## DATA VIZ

def plot_monthly_data(df_payments_year, month_choice):
    month_data = df_payments_year[df_payments_year['Month'] == month_choice]
    df_month = month_data.groupby('Labels').agg('Amount').sum()
    df_month = df_month.reset_index()
    df_month.columns = ['Labels', 'Amount']
    df_month['Amount'] = abs(df_month['Amount'])
    fig, ax = plt.subplots(figsize=(15,5))
    ax.bar(df_month['Labels'], df_month['Amount'])
    ax.tick_params(axis='x', rotation=60)
    plt.title(f"{month_choice} {df_payments_year['Year'].unique()[0]}")
    plt.ylabel('Amount €')
    plt.xlabel('Labels')
    ax.grid()
    st.pyplot(fig)


def income_vs_pay(df_deposits, df_payments_2022):
    AVAILABLE_MONTHS_2022 = df_payments_2022['Month'].unique()
    df_income = df_deposits.groupby('Month').agg('Amount').sum()
    df_payments_2022 = df_payments_2022.groupby('Month').agg('Amount').sum()
    inc_vs_pay_2022 = pd.concat([df_income, df_payments_2022], axis=1)
    inc_vs_pay_2022 = inc_vs_pay_2022.T
    inc_vs_pay_2022 = inc_vs_pay_2022[AVAILABLE_MONTHS_2022].T
    inc_vs_pay_2022.reset_index(inplace=True)
    inc_vs_pay_2022.columns = ['Month', 'Income', 'Pay']
    return inc_vs_pay_2022


def plot_inc_vs_pay(inc_vs_pay_2022):
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(inc_vs_pay_2022['Month'], inc_vs_pay_2022['Income'])
    ax.plot(inc_vs_pay_2022['Month'], abs(inc_vs_pay_2022['Pay']))
    ax.tick_params(axis='x', rotation=60)
    plt.title(f"income vs pay (Absolute Pay) 2022")
    plt.legend(['Income', 'Pay'])
    plt.ylabel('Amount')
    plt.xlabel('Months')
    ax.grid()
    st.pyplot(fig)


def comdirect_main():
    data = get_comd_data()
    processed_data = prepproc_feateng_data(data)
    df_payments, df_deposits = data_split(processed_data)
    df_payments_2021, df_payments_2022 = split_pay_year(df_payments)
    
    # full_data = st.checkbox('All transactions', key='full_data')
    # if full_data:
    #     st.table(data)
    # payments_data = st.checkbox('All Payments', key='payments')
    # if payments_data:
    #     st.table(df_payments)
    # deposits_data = st.checkbox('2022 Income', key='deposits')
    # if deposits_data:
    #     st.table(df_deposits)
        
    # MAIN MONTH SELECTION
    view_month_2022 = st.selectbox('2022 Months', df_payments_2022['Month'].unique())
    show_month_data = st.checkbox(f'View {view_month_2022} 2022')
    if show_month_data:
        st.header(f"{view_month_2022} 2022")
        plot_monthly_data(df_payments_2022, view_month_2022)
        
        view_transactions = st.checkbox(f"View {view_month_2022} 2022 transactions")
        if view_transactions:
            st.table(df_payments_2022[df_payments_2022['Month'] == view_month_2022])
        
        compare_previous_year = st.checkbox('Compare with previous year.')
        if compare_previous_year:
            st.header(f"{view_month_2022} 2021")
            plot_monthly_data(df_payments_2021, view_month_2022)
            view_transactions_prev_year = st.checkbox(f"View {view_month_2022} 2021 transactions")
            if view_transactions_prev_year:
                st.table(df_payments_2021[df_payments_2021['Month'] == view_month_2022])

    st.header('2022 BALANCE')
    inc_vs_pay_box = st.checkbox('Income vs payments 2022', key='inc_vs_pay_2022')
    if inc_vs_pay_box:
        inc_vs_pay_2022 = income_vs_pay(df_deposits, df_payments_2022)
        plot_inc_vs_pay(inc_vs_pay_2022)
        st.table(inc_vs_pay_2022)
