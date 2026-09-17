import openmeteo_requests

import pandas as pd
import math as m
import requests_cache
from retry_requests import retry

import datetime
from time import gmtime, strftime
import re

def send_info(msg):
    return print("--Weatherdata.py: " + msg + '--')
# The order of variables in hourly or daily is important to assign them correctly below
        # Setup the Open-Meteo API client with cache and retry on error
send_info("Setting up API")
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
        
url = "https://api.open-meteo.com/v1/forecast"
send_info("Set up API")

class WeatherLocation:
    """Class that holds: current temperature, min and max temps, time, chance of rain and current weather
    
    Set latitude and longitude for location
    """
    
   
    def __init__(self, latitude, longitude, name):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        
        self.current_temperature = 0
        self.daily_temperature_min = 0
        self.daily_temperature_max = 0
        self.current_weather = ''
        self.rain_chance = 0
        self.current_time = ''
        self.getData()
        
    def getData(self):
        
        
        send_info(f"Getting data for {self.name}")
        
        # Make sure all required weather variables are listed here
        params = {
	    "latitude": self.latitude,
	    "longitude": self.longitude,
        "daily": ["temperature_2m_min", "temperature_2m_max", "precipitation_probability_mean"],
	    "current": ["temperature_2m", "weather_code"],
        "timezone": "auto",
        "forecast_days": 1,
     
        }
        
        responses = openmeteo.weather_api(url, params = params)
        
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        current = response.Current()
        
        #temperature stuff
        #---------------------
        
        current_temperature_2m = current.Variables(0).Value()
        current_weather_code = current.Variables(1).Value()
        self.current_weather = self.convert_weather_code(current_weather_code)
        #rounds to 1 decimal lol
        self.current_temperature = m.floor(current_temperature_2m)
        
        
        daily = response.Daily()
        daily_temperature_2m_min = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        
        daily_precipitation_probability_mean = daily.Variables(2).ValuesAsNumpy()
        # set it to the class variables
        self.daily_temperature_min = m.floor(daily_temperature_2m_min[0])
        self.daily_temperature_max = m.floor(daily_temperature_2m_max[0])
        self.rain_chance = m.floor(daily_precipitation_probability_mean[0])
       

        #-------------------------
        
        #time stuff
        #-------------------
        # gets the timezone, example: b'GMT+3'
        timezone = str(response.TimezoneAbbreviation())
        # re.findall returns only the number from the GMT thing and then it converts it into a string, joins it together and converts it into an int
        timezone = int(''.join(map(str,re.findall(r'\d+', timezone))))  
        
        # utc0 so we can add up the timezone onto hour
        utc0 = datetime.datetime.now(datetime.timezone.utc)
        current_hour = utc0.hour + timezone
        self.current_time = datetime.datetime(utc0.year,utc0.month,utc0.day,current_hour,utc0.minute,utc0.second,utc0.microsecond).strftime("%H:%M")
        
        
        #----------------
    def convert_weather_code(self, weather_code):
        """Convert weather code and return a string, example: Sunny"""
        
        match(weather_code):
            case 0: return "Clear ☀️"
            case 1: return "Mainly clear ☀️"
            case 2: return "Partly cloudy ☁️"
            case 3: return "Overcast ☁️"
            case 45: return "Foggy ☁️"
            case 48: return "Rime fog ☁️"
            case 51: return "Light drizzle 🌧"
            case 53: return "Moderate drizzle 🌧" 
            case 55: return "Dense drizzle 🌧"
            case 56: return "Light freezing drizzle 🌧"
            case 57: return "Dense freezing drizzle 🌧"
            case 61: return "Slight rain 🌧"
            case 63: return "Moderate rain 🌧"
            case 63: return "Heavy rain 🌧"
            case 66: return "Light freezing rain"
            case 67: return "Heavy freezing rain"
            case 71: return "Slight snowfall"
            case 73: return "Moderate snowfall"
            case 75: return "Heavy snowfall"
            case 77: return "Snow grains"
            case 80: return "Slight rain shower"
            case 81: return "Moderate rain shower"
            case 82: return "Violent rain shower"
            case 85: return "Slight snow shower"
            case 86: return "Heavy snow shower"
            case 95: return "Thunderstorm"
            case 96: return "Slight hail, thunderstorm"
            case 99: return "Heavy thunderstorm \n with intense hail"
            
      
# test locations
#drachten = WeatherLocation(53.1037,6.0877, "Drachten")

#athens = WeatherLocation(37.97945, 23.71622, "Athens")



