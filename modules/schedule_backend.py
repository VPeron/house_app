# import streamlit as st
# from gsheetsdb import connect


# SHEET_URL = st.secrets["public_sheet"]

# @st.cache(ttl=600)
# def run_query(query):
#     conn = connect()
#     rows = conn.execute(query, headers=1)
#     rows = rows.fetchall()
#     return rows

# def get_schedule_data():
#     rows = run_query(f'SELECT * FROM "{SHEET_URL}"')
#     data = {
#         'day':[],
#         'Mon':[],
#         'Tue':[],
#         'Wed':[],
#         'Thu':[],
#         'Fri':[],
#         'Sat':[],
#         'Sun':[],
#         'notes':[],
#     }
#     for row in rows[:9]:
#         data['day'].append(row.day)
#         data['Mon'].append(row.Mon_b)
#         data['Tue'].append(row.Tue_c)
#         data['Wed'].append(row.Wed_d)
#         data['Thu'].append(row.Thu_e)
#         data['Fri'].append(row.Fri_f)
#         data['Sat'].append(row.Sat_g)
#         data['Sun'].append(row.Sun_h)
#         data['notes'].append(row.notes)
#     return data


# def highlight_rows(x):
#     df = x.copy()
#     # keep default black bkground
#     df.loc[:, :] = 'background-color: black'
#     # overwrite values grey color
#     df.iloc[3, :-1] = 'background-color: blue'   # lunch row
#     df.iloc[6, :-1] = 'background-color: blue'   # dinner row
#     return df 


# def apply_color(val, text_color, param):
#     color = text_color if val == param else None
#     return f'color: {color}'


# def apply_style(df):        
#     colored_df = df.style.applymap(apply_color, param='Conny+O', text_color='yellow')\
#     .applymap(apply_color, param='Kita', text_color='orange')\
#         .applymap(lambda x: "background-color: green" if x == 'Vini+O' else None).apply(highlight_rows, axis = None) 
#     st.table(colored_df)


import gspread
import streamlit as st


# hide_table_row_index = """
#                 <style>
#                 tbody th {display:none}
#                 .blank {display:none}
#                 </style>
#                 """

# # Inject CSS with Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)


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
    return df 


def apply_color(val, text_color, param):
    color = text_color if val == param else None
    return f'color: {color}'


def apply_style(df):        
    colored_df = df.style.applymap(apply_color, param='Conny+O', text_color='yellow')\
    .applymap(apply_color, param='Kita', text_color='orange')\
        .applymap(lambda x: "background-color: green" if x == 'Vini+O' else None).apply(highlight_rows, axis = None) 
    st.table(colored_df)
