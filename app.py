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

def geoCodingAPI(city):
    geoCodingURL = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWMAPI}"
    geoCodingresponse = requests.get(geoCodingURL)
    if geoCodingresponse.status_code == 200:
        geoCodingData = geoCodingresponse.json()
        latitude = geoCodingData[0]['lat']
        longitude = geoCodingData[0]['lon']
        return latitude, longitude

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
#         print(f"""--------- WEATHER DASHBOARD ---------
# -------------------------------------
# |City: {cityName}                     |
# -------------------------------------
# |Temperature: {temperature:.1f} °C               |
# -------------------------------------
# |Minimum Temperature Today: {minTemp:.1f} °C |
# -------------------------------------
# |Maximum Temperature Today: {maxTemp:.1f} °C |
# -------------------------------------
# |Humidity: {humidity}                       |   
# -------------------------------------
# |Wind Speed: {windSpeed}                   |
# -------------------------------------""")    
        dataDict = {
            "City": f"{cityName}",
            "Current Temperature": f"{temperature}",
            "Minimum Temperature Today": f"{minTemp}",
            "Maximum Temperature Today": f"{maxTemp}",
            "Humidity": f"{humidity}",
            "Wind Speed": f"{windSpeed}"
       }
        return dataDict
    else:
        print(f"Can't fetch data from OpenWeatherMap API.\nStatus Code: {owmAPIresponse.status_code}")

def featureSelection(dict, userChoice):
    if userChoice == 1:
        return {"Current Temperature": dict['Current Temperature']}
    elif userChoice == 2:
        return {"Minimum Temperature Today" : dict['Minimum Temperature Today']}
    elif userChoice == 3:
        return {"Maximum Temperature Today" : dict['Maximum Temperature Today']}
    elif userChoice == 4:
        return {
            "Humidity" : dict['Humidity']
        }
    elif userChoice == 5:
        return {
            "Wind Speed": dict['Wind Speed']
        }
    else:
        return dict
# weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1]) #default location

# weatherDataAPI(geoCodingAPI("Pakpattan")[0], geoCodingAPI("Pakpattan")[1]) #user given location

def homePage():
    userName = str(input("Enter your name: "))
    print(f"{userName}, welcome to WheaTheraPy!")
    while True:
        locationConsent = int(input("""Would you like to see weather conditions of:
                                1. Current Location
                                2. Any other City: """))
        if locationConsent != 1 and locationConsent != 2:
            print("Please either choose 1 or 2.")
            pass
        else:
            while True:
                featureConsent = int(input("""Which properties would you like to see:
                                           1. Temperature
                                           2. Minimum Temperature
                                           3. Maximum Temperature
                                           4. Humidity
                                           5. Windspeed
                                           6. All of these: """))
                if featureConsent != 1 and featureConsent != 2 and featureConsent != 3 and featureConsent != 4 and featureConsent != 5 and featureConsent != 6:
                    print("Please choose a number between 1 to 6!")
                    pass
                else:
                    break
            break
    
    if locationConsent == 1:
        result = featureSelection(weatherDataAPI(userIPdataAPI()[0], userIPdataAPI()[1]), featureConsent)
        print(f"""--------- WEATHER DASHBOARD ---------""")
        for key, value in result.items():
            try:
                numberValue = float(value)
                if '.' in str(value) and len(str(value).split('.')[1]) > 2:
                    value = f"{numberValue:.1f}"
            except ValueError:
                pass

            unit = ""

            if "Temperature" in key:
                unit = " °C"
            elif "Humidity" in key:
                unit = "%"
            elif "Wind" in key:
                unit = " m/s"
            print(f"""-------------------------------------
| {key}: {value}{unit}
-------------------------------------""")

homePage()