import requests
from datetime import datetime
from time import sleep



def get_date_time():
    
    date_today = str(datetime.now())[:10]
    time_now = str(datetime.now())[11:16]
    return date_today, time_now

 
def get_weather(city_name):
    
    api_key = "0db480ddbcf049359fc24615ce7faaf5"
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



# if __name__ == "__main__":
#     cities = ['Berlin', 'Sao Paulo', 'Alicante']
#     print(f"weather log running every hour for {[i for i in cities]}")
    
#     loop_count = 0
#     while True:
#         date_today, time_now = get_date_time()
#         if time_now.endswith(':30'):
#             for city in cities:
#                 current_temperature, feels_like, weather_description = get_weather(city)
            
#         loop_count += 1
#         print(time_now, f" - loop {loop_count}")
#         sleep(60)