import requests
from urllib.request import urlretrieve
from datetime import datetime

import streamlit as st


NASA_API_KEY = st.secrets["NASA_API_KEY"]


def fetchAPOD(date):
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    params = {
        'api_key':NASA_API_KEY,
        'date':date,
        'hd':'True'
    }
    response = requests.get(URL_APOD,params=params).json()
    try:
        st.write(f'Copyrights: {response["copyright"]}')
    except KeyError:
        st.write('No copyright available')
    st.write(f'Title: {response["title"]}')
    st.write(f'Date: {response["date"]}')
    st.write(response["explanation"])
    
    image_url = response['url']
    st.image(image_url)
    
    img_data = requests.get(image_url).content
    return img_data
    
def download_image(img_data,date_selection):
    with open(f'nasa_photos{date_selection}.jpg', 'wb') as handler:
        img_file = handler.write(img_data)
        
    with open(f'nasa_photos{date_selection}.jpg', 'rb') as whandler:
        dl_btn = st.download_button(
            label="Download image",
            data=whandler.read(img_file),
            file_name=f'nasa_photos{date_selection}.jpg',
            mime="image/png"
        )


def get_nasa_api_photos():
    st.header("Select a date to fetch photo for that day")
    date_selection = st.date_input("Date selection", max_value=datetime.today())
    img_data = fetchAPOD(date_selection)
    download_image(img_data,date_selection)
