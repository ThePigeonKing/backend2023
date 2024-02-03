import requests
import os
from datetime import datetime, timezone


def get_weather_data_for_cities(cities):
    API_KEY = get_api_key()
    weather_data = []
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(url).json()
        if response.get("weather"):
            weather = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }
            weather_data.append(weather)
        else:
            print(f"Error fetching data for {city}: {response.get('message', 'Unknown Error')}")
    return weather_data

def get_forecast_data_for_city(city):
    API_KEY = get_api_key()
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url).json()
    if response.get("list"):
        forecast_data = []
        for item in response['list']:
            forecast = {
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
            }
            forecast_data.append(forecast)
        return forecast_data
    else:
        print(f"Error fetching forecast data for {city}: {response.get('message', 'Unknown Error')}")
        return []

def get_detailed_weather_data(city_name):
    API_KEY = get_api_key()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    sunrise_time = datetime.fromtimestamp(response["sys"]["sunrise"], tz=timezone.utc)
    sunset_time = datetime.fromtimestamp(response["sys"]["sunset"], tz=timezone.utc)
    
    detailed_weather = {
        'temperature': response['main']['temp'],
        'feels_like': response['main']['feels_like'],
        'humidity': response['main']['humidity'],
        'pressure': response['main']['pressure'],
        'visibility': response['visibility'] / 1000,
        'wind_speed': response['wind']['speed'],
        'cloudiness': response['clouds']['all'], 
        'description': response['weather'][0]['description'],
        'sunrise': sunrise_time,
        'sunset': sunset_time,
    }
    icon = response["weather"][0]["icon"]
    city_name = response["name"]
    detailed_weather["name"] = city_name
    detailed_weather["icon"] = icon

    return detailed_weather

def get_lon_lat_data(city_name):
    API_KEY = get_api_key()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    lon = response["coord"]["lon"]
    lat = response["coord"]["lat"]

    return {"lon": lon, "lat": lat}

def get_api_key():
    API_KEY = os.environ.get("API_KEY", None)
    if API_KEY is None:
            raise ValueError("API_KEY is None!")
    return API_KEY