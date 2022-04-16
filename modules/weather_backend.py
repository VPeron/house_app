import requests
from datetime import datetime
import streamlit as st


def get_date_time():
    date_today = str(datetime.now())[:10]
    time_now = str(datetime.now())[11:16]
    return date_today, time_now

 
def get_weather(city_name):
    api_key = st.secrets['API_KEY']
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&" + "units=metric"
    response = requests.get(complete_url)
    x = response.json()

    try:
        y = x["main"]
        current_temperature = y["temp"]
        feels_like = y["feels_like"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
    except KeyError:
        print(" City Not Found ")  
    return current_temperature, feels_like, weather_description
