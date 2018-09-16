from geopy.geocoders import Nominatim
from joint_build_database import monther, locales
import json
import requests

def identify_people(Session, json_name):
    session = Session()
    session.query(monther).delete()
    geolocator = Nominatim(user_agent="showtime3")

    with open(json_name) as mlist:
        data = json.load(mlist)
    print(data)
    for line in data:
        city = data[line]['city']
        state = data[line]['state']
        email = data[line]['email']
        radius = data[line]['radius']
        try:
            lat = data[line]['lat']
            long = data[line]['long']
        except:
            #but Google Maps API is not working
            a = city + ', ' + state
            map_string = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city + '+' + state
            response = requests.get(map_string)
            resp_json_payload = response.json()
            x_ll = resp_json_payload['results'][0]['geometry']['location']
            lat = x_ll['lat']
            long = x_ll['lng']
        sig = city+state+radius
        newmonther = monther(email=email, city=city, state=state, lat=lat, long=long, radius=radius, sig=sig)
        q = session.query(monther).filter(monther.email == newmonther.email, monther.city == newmonther.city)
        check = (session.query(q.exists()).scalar())
        if check == False:
            print(("Adding {0}").format(line))
            session.add(newmonther)
    session.commit()

def identify_places(Session):
    session = Session()
    session.query(locales).delete()
    monthers = session.query(monther)

    for person in monthers:
        k = session.query(locales).filter(locales.lat == person.lat,
                                          locales.long == person.long, locales.radius == person.radius)
        if k.first() == None:
            newlocale = locales(lat=person.lat, long=person.long, radius=person.radius,
                                city=person.city, state=person.state)
            newlocale.sig = newlocale.uniq_id()
            print(newlocale.sig)
            print(("Adding new locale: {0}, {1}: {2} miles".format(newlocale.city, newlocale.state, newlocale.radius)))
            session.add(newlocale)
    session.commit()

    k = session.query(locales)
    for i in k:
        q = session.query(monther).filter(monther.lat == i.lat, monther.long == i.long,
                                          monther.radius == i.radius)
        for person in q:
            person.sig = i.sig

    session.commit()