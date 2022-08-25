import logging

import streamlit as st
import pandas as pd


from modules.weather_backend import get_weather, get_date_time
from modules.crypto_backend import monitor_ranges, plot_data
from modules.schedule_backend import get_schedule_data, apply_style
from modules.news_backend import get_news_api, view_sources
from modules.comdirect_backend import comdirect_main
from modules.nasa_api_backend import get_nasa_api_photos


FRONT_PASSWORD = st.secrets["FRONT_PASSWORD"]

st.set_page_config(page_title='House Page', page_icon="🔒", layout='centered')


def front_door():
    session_state = False
    
    main_col_1, main_col_2, main_col_3 = st.columns([1,4,1])
    with main_col_1:
        st.write('')
    
    with main_col_2:
        front_placeholder = st.empty()
        front_placeholder.title(' ☘ « ※ » ♠🔒♠ « ※ » ☘')
        ## AUTHENTICATION ##
        placeholder = st.empty() 
        input_password = placeholder.text_input(' 🔑 :', value='', type='password')
        if input_password:
            if input_password == FRONT_PASSWORD:
                session_state = True
                    
                front_placeholder.empty()
                placeholder.empty()
            else:
                placeholder.image('https://www.how-to-draw-funny-cartoons.com/image-files/cartoon-chair-6.gif')
                logging.warning("Failed login attempt.")
                session_state = False
                st.stop()
        
    with main_col_3:
        st.write('')

    return session_state


def home_page():
    # st.title('☘♡⚤«♚♠ Home Page ♠♚»☮♡☘')
    # WEATHER WIDGET
    city = st.sidebar.selectbox("Select a city", ['Berlin', 'Sao Paulo', 'Alicante'])
    if city:
        try:
            current_temperature, feels_like, weather_description = get_weather(city)
            st.sidebar.info(f"""{city}\n
Temperature: {current_temperature}\n
Feels like: {feels_like}\n
{weather_description}""")
        except KeyError:
            st.error('There was an error (KeyError), please try again.')
            logging.warning('Weather widget Key error.')
    
     # SCHEDULE WIDGET
    st.title('Schedule')
    # CSS variable to remove streamlit default table index
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    
    list_of_lists = get_schedule_data()
    result_table = pd.DataFrame(list_of_lists)
    result_table.columns = [i for i in pd.DataFrame(result_table).T[0]] # insert header as table header
    apply_style(result_table[1:])  # display styled table without header
    

def news_page():
    st.title("News")
    st.sidebar.image('https://nsiteam.com/social/wp-content/uploads/2016/12/Depositphotos_19723583_m-2015-930x698.jpg')
    search_news = st.text_input("Keyword search NewsApi:")
    if search_news:
        get_news_api(search_news)
    
    view_all_sources = st.checkbox('view all sources')
    st.sidebar.info('Current Filter: bbc-news,the-verge,bloomberg,hacker-news,wired,wired-de,el-mundo,die-zeit,der-tagesspiegel')
    if view_all_sources:
        view_sources()


def crypto_page():
    st.title('Crypto Data')
    st.sidebar.image('https://wallpapercave.com/wp/wp4678546.jpg')
    crypto_data = monitor_ranges()
    plot_data(crypto_data)
    

def comd_page():
    st.sidebar.image('https://is2-ssl.mzstatic.com/image/thumb/Purple113/v4/86/3e/20/863e2097-3761-df35-0537-4ffb77fd8dc3/source/512x512bb.jpg')
    comdirect_main()
    
def nasa_api():
    st.title('Photos provided by api.nasa.gov API.')
    get_nasa_api_photos()


def main():
    date_today = get_date_time()[0]
    st.sidebar.info(f"{date_today}")
    # Register your pages
    pages = {
        "Homepage": home_page,
        "News": news_page,
        "Cryptocurrencies": crypto_page,
        "Comdirect":comd_page,
        "Nasa Photos":nasa_api,
        #"About": about_page,
        #"Contact": contact_page,
    }
    
    
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))
    pages[page]()
    
    
if __name__ == "__main__":
    base_auth = front_door()
    if base_auth:
        main()
