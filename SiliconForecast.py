#importing requests and BeautifulSoup and pandas modules
import requests
import pandas as pd
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
'''period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()
'''

#extracting the title which is inside the img tag
'''img = tonight.find("img")
desc = img['title']'''

''' Select all items with the class period-name inside an item with the class tombstone-container in seven_day.
 Use a list comprehension to call the get_text method on each BeautifulSoup object.'''
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]

#same way to get all the three fields
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

#printing the same
'''print(periods)
print(short_descs)
print(temps)
print(descs)'''
'''print(short_desc)
print(temp)
print(desc)'''

#now, combining our data into a Pandas frame and printing them
weather = pd.DataFrame({
	"period":periods,
	"short_desc":short_descs,
	"temp":temps,
	"desc":descs
	})
print (weather)
