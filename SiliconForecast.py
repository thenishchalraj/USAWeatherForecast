#importing requests and BeautifulSoup
import requests
from bs4 import BeautifulSoup

#get the page as a response with all the details
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.37&lon=-122.04")

#parsing the page to get the useful content
soup = BeautifulSoup(page.content, 'html.parser')

#finding the useful info extracting from the page content
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")

#getting the forecast about a particular time from the particular place/element
tonight = forecast_items[0]

#extracting the data for tonight
period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

#printing the same
print(period)
print(short_desc)
print(temp)
