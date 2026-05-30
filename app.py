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

def weatherDataAPI(defaultLat, defaultLon):
    owmURL = f"https://api.openweathermap.org/data/2.5/weather?lat={defaultLat}&lon={defaultLon}&appid={OWMAPI}"
    owmAPIresponse = requests.get(owmURL)
    if owmAPIresponse.status_code == 200:
        owmAPIdata = owmAPIresponse.json()
        print(owmAPIdata)
        cityName = owmAPIdata['name']
        temperature = owmAPIdata['main']['temp'] - 273.15
        minTemp = owmAPIdata['main']['temp_min'] - 273.15
        maxTemp = owmAPIdata['main']['temp_max'] -273.15
        humidity = owmAPIdata['main']['humidity']
        windSpeed = owmAPIdata['wind']['speed']
        longitude = owmAPIdata['coord']['lon']
        latitude = owmAPIdata['coord']['lat']
        print(f"""City: {cityName}
Temperature:{temperature:.1f} °C
Minimum Temperature Today: {minTemp:.1f} °C
Maximum Temperature Today: {maxTemp:.1f} °C
Humidity: {humidity}
Wind Speed: {windSpeed}""")
        return latitude, longitude
    else:
        print(f"Can't fetch data from OpenWeatherMap API.\nStatus Code: {owmAPIresponse.status_code}")

def aqiDataAPI(lat, lon):
    aqiAPIURL = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQIAPI}"
    aqiAPIresponse = requests.get(aqiAPIURL)
    if aqiAPIresponse.status_code == 200:
        aqiAPIData = aqiAPIresponse.json()
        print(aqiAPIData)
    else:
        print(f"Can't fetch Data from API.\nStatus Code: {aqiAPIresponse.status_code}")

# weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1])

# userIPdataAPI()

aqiDataAPI(weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1])[0], weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1])[1])