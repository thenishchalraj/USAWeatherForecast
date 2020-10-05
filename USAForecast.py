# Importing the Required Python libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse
from toAscii import ConvertImages
from covidReporter import Reports

soup = ""
class WeatherInfo():
    disclaimer = """
This script is only for educational purpose. 
Please do check your region's law & regulations before web scraping any website.
    """

    print(disclaimer, "\n\n")

    def __init__(self, address):
        self.address = address
        self.URL = ""
        self.timeperiods = []
        self.temperatures = []
        self.short_descriptions = []
        self.descriptions = []

    def parsedata(self):
        global soup
        # Fetching geo-coordinates for the address
        openstreetmap_url = f'https://nominatim.openstreetmap.org/search/{urllib.parse.quote(self.address)}?format=json'
        map_json_data = requests.get(openstreetmap_url).json()

        # Sending a get request and parsing the webpage
        URL = f'https://forecast.weather.gov/MapClick.php?lat={urllib.parse.quote(map_json_data[0]["lat"])}&lon={urllib.parse.quote(map_json_data[0]["lon"])}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extracting the essential data from the scraped data

        seven_days_forecast = soup.find(id="seven-day-forecast")
        if not bool(seven_days_forecast):
            print("Can't find the place")
            return

        # Filtering Raw Data from variable seven_days_forecast

        # Extracting Time Periods Data for the following seven days

        timeperiod_tags = seven_days_forecast.select(".tombstone-container .period-name")
        self.timeperiods = [timeperiod.get_text() for timeperiod in timeperiod_tags]

        # Extracting Temperatures Data for the following seven days

        temperature_tags = seven_days_forecast.select(".tombstone-container .temp")
        self.temperatures = [temperature.get_text() for temperature in temperature_tags]

        # Extracting Short Descriptions Data for the following seven days

        short_description_tags = seven_days_forecast.select(".tombstone-container .short-desc")
        self.short_descriptions = [short_description.get_text() for short_description in short_description_tags]

        # Extracting Description for the following seven days

        self.descriptions = [description["title"] for description in
                             seven_days_forecast.select(".tombstone-container img")]
        
        self.imgs = ConvertImages(soup)

        return self.timeperiods, self.short_descriptions, self.temperatures, self.descriptions, self.imgs

    def pandas_data(self):
        # Generating the Pandas DataFrame from the data output from function 'parsedata'

        self.weather_data = pd.DataFrame({
            "Time Period": self.timeperiods,
            "Temperature": self.temperatures,
            "Short Description": self.short_descriptions,
            "Description": self.descriptions,
        })

        return self.weather_data  # Remove .head, if you wish to preview all the extracted data

    def pandas_to_csv(self):
        # Converting the Pandas DataFrame data in the Comma Separated Value format.

        return self.weather_data.to_csv("Weather_Forecast.csv")


# Calling the class WeatherInfo() and providing geo-coordinates (e.g. latitude, longitude) of the location

location = input("Please enter location: ")
us_weather = WeatherInfo(location)

# Calling the Class function 'parsedata' and Printing the extracted data

us_weather.parsedata()

# To print the data from function parsedata(), then use print function as shown in the below line command
# print(san_francisco_weather.parsedata())

print("""
    
   __  _______ ___       _       __           __  __                 ______                                __ 
  / / / / ___//   |     | |     / ___  ____ _/ /_/ /_  ___  _____   / ________  ________  _________ ______/ /_
 / / / /\__ \/ /| |     | | /| / / _ \/ __ `/ __/ __ \/ _ \/ ___/  / /_  / __ \/ ___/ _ \/ ___/ __ `/ ___/ __/
/ /_/ /___/ / ___ |     | |/ |/ /  __/ /_/ / /_/ / / /  __/ /     / __/ / /_/ / /  /  __/ /__/ /_/ (__  / /_  
\____//____/_/  |_|     |__/|__/\___/\__,_/\__/_/ /_/\___/_/     /_/    \____/_/   \___/\___/\__,_/____/\__/  
                                                                                                              
                                                                    -By thenischalraj
                                                                        Sourced from forecast.weather.gov
""")


print(us_weather.pandas_data())
print("\n")
Reports(location)

# To save the weather report in Comma Separated Value format (aka .csv), just uncomment the below line command

# san_francisco_weather.pandas_to_csv()