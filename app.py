# ask user about location -> default vs input -> ask user what to see in it -> current temp, max temp, min temp, humidity, wind speed -> option for selecting multiple -> display that

from dotenv import load_dotenv
import os, requests

load_dotenv()

WAQIAPI = os.getenv("WAQI_API")
OWMAPI = os.getenv("OPEN_WEATHER_MAP_API")

ipAPIURL = "http://ip-api.com/json/"

def userIPdataAPI():
    ipAPIrespose = requests.get(ipAPIURL)
    if ipAPIrespose.status_code == 200:
        ipAPIdata = ipAPIrespose.json()
        defaultLat = ipAPIdata['lat']
        defaultLon = ipAPIdata['lon']
        cityName = ipAPIdata['city']
        # print(ipAPIdata)
        return defaultLat, defaultLon, cityName
    else:
        print(f"Failed to fetch data: {ipAPIrespose.status_code}")

def weatherDataAPI(Lat, Lon):
    owmURL = f"https://api.openweathermap.org/data/2.5/weather?lat={Lat}&lon={Lon}&appid={OWMAPI}"
    owmAPIresponse = requests.get(owmURL)
    if owmAPIresponse.status_code == 200:
        owmAPIdata = owmAPIresponse.json()
        # print(owmAPIdata)
        cityName = owmAPIdata['name']
        temperature = owmAPIdata['main']['temp'] - 273.15
        minTemp = owmAPIdata['main']['temp_min'] - 273.15
        maxTemp = owmAPIdata['main']['temp_max'] -273.15
        humidity = owmAPIdata['main']['humidity']
        windSpeed = owmAPIdata['wind']['speed']
        longitude = owmAPIdata['coord']['lon']
        latitude = owmAPIdata['coord']['lat']
        print(f"""--------- WEATHER DASHBOARD ---------
-------------------------------------
|City: {cityName}                     |
-------------------------------------
|Temperature: {temperature:.1f} °C               |
-------------------------------------
|Minimum Temperature Today: {minTemp:.1f} °C |
-------------------------------------
|Maximum Temperature Today: {maxTemp:.1f} °C |
-------------------------------------
|Humidity: {humidity}                       |   
-------------------------------------
|Wind Speed: {windSpeed}                   |
-------------------------------------""")                 
    else:
        print(f"Can't fetch data from OpenWeatherMap API.\nStatus Code: {owmAPIresponse.status_code}")

weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1]) #default location

userIPdataAPI()