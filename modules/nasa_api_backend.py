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
    st.write(response)
    # try:
    #     st.write(f'Copyrights: {response["copyright"]}')
    # except KeyError:
    #     st.write('No copyright available')
    # st.write(f'Title: {response["title"]}')
    # st.write(f'Date: {response["date"]}')
    # st.write(response["explanation"])
    
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
    
    date_selection = st.date_input("Select a date for photo of that date?", max_value=datetime.today())
    img_data = fetchAPOD(date_selection)
    placeholder = st.empty()
    download_button = placeholder.button('Prepare image download?', key="download trigger")
    
    if download_button:
        placeholder.empty()
        download_image(img_data,date_selection)
    
  
# if __name__ == "__main__":
#     get_nasa_api_photos()