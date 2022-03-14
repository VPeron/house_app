import streamlit as st
from modules.weather_backend import get_weather, get_date_time


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
                session_state = False
                st.stop()
        
    with main_col_3:
        st.write('')

    return session_state


def home_page():
    date_today, time_now = get_date_time()
    st.title('☘♡⚤«♚♠ Home Page ♠♚»☮♡☘')
    st.info(date_today)
    city = st.selectbox("Select a city", ['Berlin', 'Sao Paulo', 'Alicante'])
    if city:
        try:
            current_temperature, feels_like, weather_description = get_weather(city)
            st.info(f"""{city}\n
Temperature:{current_temperature}\n
Feels like {feels_like}\n
{weather_description}""")
        except KeyError:
            st.error('There was an error (KeyError), please try again.')
    

def first_page():
    st.title('First Page')
   

def about_page():
    st.title('About')



def contact_page():
    st.title('Contact')
    st.info("viperon.python@gmail.com")
        

def main():
    # Register your pages
    pages = {
        "Homepage": home_page,
        "First Page": first_page,
        "About": about_page,
        "Contact": contact_page,
    }
    
    page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))
    pages[page]()
    
    
if __name__ == "__main__":
    base_auth = front_door()
    
    if base_auth:
        main()
        
    
