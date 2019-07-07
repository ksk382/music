from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from geopy.geocoders import Nominatim

db = declarative_base()

class locales(db):
    __tablename__ = 'locales'

    id = Column(Integer, primary_key=True)
    city = Column(String(64), index=True)
    state = Column(String(8), index=True)
    radius = Column(Integer)
    lat = Column(String(20))
    long = Column(String(20))
    sig = Column(String(20))

    '''def __init__(self, locale):
        a = locale.split(' ')
        self.locale = locale
        self.city = a[0]
        self.state = a[1]'''

    def getlatlong(self):
        geolocator = Nominatim()
        a = self.city + ',' + self.state
        location = geolocator.geocode(a, timeout=4)
        self.lat = str(location.latitude)
        self.long = str(location.longitude)
        a = '(' + self.lat + ', ' + self.long + ')'
        return a

    def uniq_id(self):
        x = self.city + self.state + str(self.radius)
        return x

class band(db):
    __tablename__ = 'band'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    song = Column(String(64))
    album = Column(String(64))
    appeared = Column(String(64), index=True)
    cleanname = Column(String(64), index=True)
    source = Column(String(64), index=True)
    dateadded = Column(String(64), index=True)
    comment = Column(String(64), index=True)
    spotify_id = Column(String(64), index=True)
    google_play_id = Column(String(64), index=True)

    def __repr__(self):
        return '<Table Name: %s>' % self.name

class monther(db):
    __tablename__ = 'monther'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), index=True)
    city = Column(String(64), index=True)
    state = Column(String(8), index=True)
    radius = Column(Integer)
    lat = Column(String(20))
    long = Column(String(20))
    sig = Column(Integer)

    def __repr__(self):
        return '<Monther: % s>' % self.name

class gig(db):
    __tablename__='gig'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    cleanname = Column(String(64), index=True)
    date = Column(String(64), index=True)
    venue = Column(String(64), index=True)
    city = Column(String(64), index=True)
    source = Column(String(64), index=True)
    queryby = Column(String(64), index=True)
    dateadded = Column(String(64), index=True)

    def __repr__(self):
        x = str(self.city + ' ' + self.venue + ' ' +  self.date + ' ' +  self.source + ' ' +  self.queryby)
        return x
