from joint_concert_finder import grabBIT, grabTFLY
from joint_build_database import locales, band, gig
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database import db
from gsheetpull import sheetpull

def gettheshows(Session):
    session = Session()
    bandlist = session.query(band)
    places = session.query(locales)
    t = dt.date.today()

    showlist = grabBIT(bandlist, places)
    for i in showlist:
        q = session.query(gig).filter(gig.date == i.date, gig.cleanname == i.cleanname)
        if q.first() == None:
            try:
                print(("Adding {0} at {1} on {2} (from {3})".format(i.name, i.venue, i.date, 'Bandsintown')))
            except:
                print ('Added unprintable show from Bandsintown')
            i.dateadded = t
            session.add(i)
            session.commit()


    return

if __name__ == "__main__":
    v = sheetpull()
    print (v)
    print (len(v))