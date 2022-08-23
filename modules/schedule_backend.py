import gspread
import streamlit as st


def get_schedule_data():
    gc = gspread.service_account_from_dict(st.secrets['GCP_CREDENTIALS'])

    sh = gc.open("current_schedule")
    worksheet = sh.sheet1

    list_of_lists = worksheet.get_all_values()
    return list_of_lists


def highlight_rows(x):
    df = x.copy()
    # keep default black bkground
    df.loc[:, :] = 'background-color: black'
    # overwrite values grey color
    df.iloc[3, :-1] = 'background-color: blue'   # lunch row
    df.iloc[6, :-1] = 'background-color: blue'   # dinner row
    try:
        df.iloc[13, :-1] = 'background-color: blue'   # lunch row
        df.iloc[16, :-1] = 'background-color: blue'   # dinner row
    except IndexError:
        pass
    return df


def apply_color(val, text_color, param):
    color = text_color if val == param else None
    return f'color: {color}'


def apply_style(df):        
    colored_df = df.style.applymap(apply_color, param='Conny+O', text_color='yellow')\
    .applymap(apply_color, param='Kita', text_color='orange')\
        .applymap(apply_color, param='Vini+O', text_color='green').apply(highlight_rows, axis = None) 
    st.table(colored_df)