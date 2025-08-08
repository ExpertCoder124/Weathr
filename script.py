#version 0.1
import time
import re
import os
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests 
from bs4 import BeautifulSoup
import json
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

#This will not run on an online IDE!! 
 
Y = 'Null'

def clr(): #clears everything from terminal
    if (os.name) == 'nt':
        os.system("cls")
    else:
        os.system("clear")
clr()
load_scr = 'false' #Circumnagivate built-in rate limiting. Set to true for loading screen

# print ('Weathr') WIP
# Make 'Weathr' bigger in console

if load_scr == 'true' :
    for i in range(1,4):
        print ('Weathr')
        print ('Loading.')
        time.sleep(5/9)
        clr()
        print ('Weathr')
        print ('Loading..')
        time.sleep(5/9)
        clr()
        print ('Weathr')
        print ('Loading...')
        time.sleep(5/9)
        clr()
#NWS has an API limit of 1 request per 5 seconds
# End of startup

# Finding where the user lives. Location API will be implimented in the future

input_loc = input ('Enter a location : ')

address = Nominatim(user_agent="GetLoc")

loc = address.geocode(input_loc)

str_loc = str(loc)

In_US = str_loc.find("United States")# Searches to see if location is inside the United States

if In_US == -1:
    print('Sorry, weather data outside of the United States is unavalible at the moment.') 
    Y = input('Enter "Y" to exit ')
    if Y == 'Y':     
        quit()

else:
    print('Displaying Weather for ' + loc.address)

Lat = str(loc.latitude)
Long = str(loc.longitude) # Coordinates
print(Lat + Long)

# Taking the Data from NWS API
headers = {'User-Agent' : "Weathr"} 
URL_nonstr = ("https://api.weather.gov/points/"+ Lat + ',' + Long) 
URL = str(URL_nonstr)
r = requests.get(url=URL, headers=headers) 
raw_soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib 

#turning HTML into plain text
cooked_soup = raw_soup.get_text()
xydata = json.loads(cooked_soup)
xydata = dict(xydata)


weatherURL = ((xydata['properties']["forecast"]))

headers = {'User-Agent' : "Weathr"} 
URL_nonstr = (weatherURL) 
URL = str(URL_nonstr)
r = requests.get(url=URL, headers=headers) 
raw_soup = BeautifulSoup(r.content, 'html.parser') 


cooked_soup = raw_soup.get_text()
weather_data = json.loads(cooked_soup)
weather_data = dict(weather_data)
print((weather_data['properties']['periods']))



