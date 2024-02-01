import os

import geonamescache
import requests


def get_weather_data(city):
    # TODO вынести в .env файл
    api_key = os.getenv("APIKEY", None)
    if api_key is None:
        raise ValueError("API key not defined!")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(complete_url)
    rsp = response.json()
    # print(rsp)
    return rsp


def get_city_choices(minpopulation=1_000_000):
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    large_cities = {
        key: val for key, val in cities.items() if val["population"] > minpopulation
    }
    sorted_cities = sorted(large_cities.values(), key=lambda x: x["name"])
    # tuple for drop down menu
    city_choices = [(city["name"], city["name"]) for city in sorted_cities]
    return city_choices
