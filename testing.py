from geopy.geocoders import Nominatim
from joint_build_database import monther, locales
import json
import requests


city = 'San Francisco'
state = 'CA'
map_string = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city + '+' + state
response = requests.get(map_string)

resp_json_payload = response.json()

x_ll = resp_json_payload['results'][0]['geometry']['location']
lat = x_ll['lat']
long = x_ll['lng']


'''
geolocator = Nominatim(user_agent="showtime3")

city = 'San Francisco'
state = 'CA'
a = city + ', ' + state
print (a)
location = geolocator.geocode(a, timeout=4)
lat = location.latitude
long = location.longitude
print (lat, long)
print (geolocator.timeout)
'''