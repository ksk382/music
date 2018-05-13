from geopy.geocoders import Nominatim
from joint_build_database import monther, locales
import json

def identify_people(Session, json_name):
    session = Session()
    session.query(monther).delete()
    geolocator = Nominatim()

    with open(json_name) as mlist:
        data = json.load(mlist)
    print(data)
    for line in data:
        city = data[line]['city']
        state = data[line]['state']
        email = data[line]['email']
        radius = data[line]['radius']
        a = city + ',' + state
        location = geolocator.geocode(a, timeout=4)
        lat = location.latitude
        long = location.longitude
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