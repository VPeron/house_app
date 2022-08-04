import streamlit as st
import pandas as pd
import logging

from modules.weather_backend import get_weather, get_date_time
from modules.crypto_backend import monitor_ranges, plot_data
from modules.schedule_backend import get_schedule_data, apply_style
from modules.news_backend import get_news_api, view_sources
from modules.comdirect_backend import get_comd_data, pre_proc_data ,plot_monthly_data
from modules.nasa_api_backend import get_nasa_api_photos

FRONT_PASSWORD = st.secrets["FRONT_PASSWORD"]

st.set_page_config(page_title='House Page', page_icon="🔒", layout='centered')

# to configure the logger further you can use basicConfig()
# but if this gets more complex its better to also implement a handler.
# logging.basicConfig(filename='request_site_status.log', level=logging.DEBUG,
#                     format='%(asctime)s:%(name)s:%(message)s')
# logging.debug(f'Display debug message.')

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
    date_today, time_now = get_date_time()
    # st.title('☘♡⚤«♚♠ Home Page ♠♚»☮♡☘')
    st.info(f"{date_today} at {time_now}")
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
    
    st.title('Schedule')
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    data = get_schedule_data()
    df = pd.DataFrame(data)
    apply_style(df)
    

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
    raw_df = get_comd_data()
    df = pre_proc_data(raw_df)
    
    years_available = set(df['Date'].dt.year.to_list())
    select_year = st.selectbox('Choose a year', years_available)
    df_year = df[df['Date'].dt.year == select_year]
    
    months_available = set(df_year['Date'].dt.month_name().to_list())
    select_month = st.selectbox('Choose a month', months_available)
    df_month = df_year[df_year['Date'].dt.month_name() == select_month]
    
    transactions = st.checkbox('View transactions')
    if transactions:
        st.write(df_month)
    st.header('Summary Table')
    month_summary = df_month.groupby('Labels').agg('Amount').sum()
    st.write(month_summary)
    plot_monthly_data(month_summary, select_month, select_year)
    
def nasa_api():
    st.title('Photos provided by NASA API.')
    get_nasa_api_photos()
    
   

def about_page():
    st.title('About')
    st.sidebar.write('[Github](https://github.com/VPeron/house_app)')
    st.info("""
            Family playground.
            """)
    st.image("https://wp-media.patheos.com/blogs/sites/576/2088/01/matrix-city.jpg")


def contact_page():
    st.title('Contact')
    st.info("viperon.python@gmail.com")
        

def main():
    # Register your pages
    pages = {
        "Homepage": home_page,
        "News": news_page,
        "Crypto Data": crypto_page,
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
