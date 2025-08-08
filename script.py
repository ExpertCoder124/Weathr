version = '0.1'
debug = False #Debug will skip entering a location, and sets location to New York City
#TODO
#Add rate limiting
#Add splash screen 
#NWS has an API limit of 1 request per 5 seconds
#Automatically figure out user location
#Add worldwide forecast
#auto install required apps
#create a dict to more easily manage JSON dict mess
#add a forecast last updated thingy, convert from iso 8601 to timezone
#find a way to check if place requested even exists, not just exists outside of USA


import requests #for scraping NWS API
import os #for the clr function
import sys #for stopping program in case of error
import subprocess #for installing pip apps
import time #so people can read text between processes



def clr(): #clears everything from the terminal
    if (os.name) == 'nt':
        os.system("cls")
    else:
        os.system("clear")
clr()

try:
  from geopy.geocoders import Nominatim #for finding coords of location

except ModuleNotFoundError:#in the case that the nominatim module isn't installed
  #auto installs module
  print('The pip module "GeoPy" is required to run the Weather app.')
  print('GeoPy is used to convert locations into machine-readable GPS coordinates')
  print('The GeoPy module cannot find or track your current location.')
 
  givenAnswer = False 
  while givenAnswer == False: #checks to see if user actually gave answer
    install_yes_or_no = input('Would you like to install GeoPy in this Python virtual enviroment? (Y/n) ')
  
    if install_yes_or_no.lower() == 'y':#.lower() turns capital Y into lowercase y
      #this allows me to check both Y and y
      clr()
      print('Installing app...')
      subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
      from geopy.geocoders import Nominatim #init package
      clr()
      givenAnswer = True
      print('App has been successfully installed! Loading weather app...')
      time.sleep(3)

    elif install_yes_or_no.lower() == 'n':
      givenAnswer == True
      clr()
      print('Sorry, but GeoPy is required to use the Weather app.')
      sys.exit('App has been exited.')
      
    else:

      print('Your response ("' + install_yes_or_no + '") was not one of the expected responses: Y or n')


def scrape(URL): #Scrapes NWS to turn JSON to Dict
    # The 'requests' and 'sys' module must be imported
    # Use like this: var1 = scrape('https://api.weather.gov/points/40.7127281,-74.0060152')
  try:
    r = requests.get(str(URL))

  except requests.exceptions.ConnectionError:#error code for not connected to the internet
    print("You don't seem to be connected to the internet.")
    print("Check your network connection, and launch the app to try again.")
    sys.exit('Program Stopped')
  
  if r.status_code != 200: #in case anything else goes wrong
    return 'HTTP status code ' + str(r.status_code)
    print('Something went wrong.')
    print('Connecting to the servers failed with HTTP status code ' + r.status_code)
    sys.exit()

  return r.json()

clr()
if debug == True:

    input_loc = 'New York City'
else:
    print('Only locations in the US are supported right now')
    input_loc = input ('Enter a location: ')

address = Nominatim(user_agent="GetLoc")
loc = address.geocode(input_loc)
str_loc = str(loc)
In_US = str_loc.find("United States")# Searches to see if location is inside the United States
if In_US == -1:
    print('Sorry, weather data outside of the United States is unavalible at the moment.') 
    sys.exit('Relaunch the app to search again')

else:
    print('Displaying Weather for ' + loc.address)

Lat = str(loc.latitude)
Long = str(loc.longitude) # Coordinates


forecastGridpoints = scrape(str("https://api.weather.gov/points/"+ Lat + ',' + Long))
#refer to NWS API documentation for information on gridpoints
forecastURL = forecastGridpoints["properties"]["forecast"] 
#hourlyForecastURL = forecastGridpoints["properties"]["forecastHourly"]
#hourly forecast will be added in a future update

forecast = scrape(str(forecastURL))
#forecast is now a JSON-Style dictonary! WOOHOO!

forecastlastupdated = forecast["properties"]["updateTime"]
# variable showing the last time the forecast was updated

for i in range (0,14):
    print('The weather ' + (forecast["properties"]["periods"][i]["name"]) + ' will be' )
    print((forecast["properties"]["periods"][i]["detailedForecast"]) + '\n')

print('Relaunch the app to see another place!')
print('App version ' + version)
while debug == False or debug == True: 
  if debug == True:
    print('Debug mode is on.')
  #infinite loop here because I don't know what to do after this
