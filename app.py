import requests, time

OWMAPI = input("Please enter your OpenWeatherMap API Key: ")

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

def forecastChecking(lat, lon):
    ForecastAPIUrl = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OWMAPI}"
    forecastResponse = requests.get(ForecastAPIUrl)
    if forecastResponse.status_code == 200:
        forecastData = forecastResponse.json()
        
        forecastDict = {}

        for i in forecastData['list']:
            timeStamp = i['dt_txt']
            tempCelsius = i['main']['temp'] - 273.15
            forecastDict[timeStamp] = f"{tempCelsius:.1f}"
        
        return forecastDict
    else:
        print(f"Error fetching data.\nStatus Code: {forecastResponse.status_code}")
        return {}

def featureSelection(dict, userChoice, lat=None, lon=None):
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
    elif userChoice == 6:
        return dict
    else:
        return forecastChecking(lat, lon)

def homePage():
    userName = str(input("Enter your name: "))
    print(f"{userName}, welcome to WheaTheraPy!")
    while True:
        locationConsent = int(input("Would you like to see weather conditions of:\n1. Current Location\n2. Any other City: "))
        if locationConsent != 1 and locationConsent != 2:
            print("Please either choose 1 or 2.")
            pass
        else:
            while True:
                featureConsent = int(input("Which properties would you like to see:\n1. Temperature\n2. Minimum Temperature\n3. Maximum Temperature\n4. Humidity\n5. Windspeed\n6. All of above\n7. 5-Days Forecast: "))
                if featureConsent != 1 and featureConsent != 2 and featureConsent != 3 and featureConsent != 4 and featureConsent != 5 and featureConsent != 6 and featureConsent != 7:
                    print("Please choose a number between 1 to 7!")
                    pass
                else:
                    break
            break
    
    if locationConsent == 1:
        lat, lon, city = userIPdataAPI()
        result = featureSelection(weatherDataAPI(lat, lon), featureConsent, lat=lat, lon=lon)
        print(f"""--------- WEATHER DASHBOARD ---------""")
        for key, value in result.items():
            if "-" in key and ":" in key:
                print(f"| {key}: {value} °C")
                print("-------------------------------------")
                time.sleep(2)
            else:
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
                print(f"-------------------------------------\n| {key}: {value}{unit}\n-------------------------------------")
                time.sleep(2)
    elif locationConsent == 2:
        cityName = input("Enter the city name: ")
        latitude = geoCodingAPI(cityName)[0]
        longitude = geoCodingAPI(cityName)[1]
        weatherData = weatherDataAPI(latitude, longitude)
        result = featureSelection(weatherData, featureConsent,lat=latitude, lon=longitude)
        print(f"""--------- WEATHER DASHBOARD ---------""")
        for key, value in result.items():
            if "-" in key and ":" in key:
                print(f"| {key}: {value} °C")
                print("-------------------------------------")
                time.sleep(2)
            else:
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
                print(f"-------------------------------------\n| {key}: {value}{unit}\n-------------------------------------")
                time.sleep(2)

homePage()