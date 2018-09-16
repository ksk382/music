from geopy.geocoders import Nominatim
from joint_build_database import monther, locales
import json
import requests
import urllib
import googlemaps

#https://github.com/googlemaps/google-maps-services-python

api_key = 'AIzaSyAQs_nHOt9cUO4szFj3jJ1e_NqX6YN47cA'

def latlong(g):
    f = urllib.parse.urlencode(g)
    map_string = 'https://maps.googleapis.com/maps/api/geocode/json?' + f + '&key=' + api_key
    print (map_string)
    response = requests.get(map_string)
    resp_json_payload = response.json()
    print ('\n\n\n')
    print (resp_json_payload)
    print ('\n\n\n')
    print (resp_json_payload['results'])
    x_ll = resp_json_payload['results'][0]['geometry']['location']
    lat1 = x_ll['lat']
    long1 = x_ll['lng']

    print (lat1, long1)
    return lat1, long1



address = '400 7th St SW'
city = 'washington'
state = 'DC'
g = {'address': address, 'city':city,'state':state}
lat1, long1 = latlong(g)

address = '501 Seward Sq SE'
city = 'washington'
state = 'DC'
g = {'address': address, 'city':city,'state':state}
lat2, long2 = latlong(g)


orig_coord = lat1, long1
dest_coord = lat2, long2
url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
response = requests.get(url)
result = response.json()
driving_time = result['rows'][0]['elements'][0]['duration']['value']
print ('driving time: ', driving_time)