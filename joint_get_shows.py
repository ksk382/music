from joint_concert_finder import grabBIT, grabTFLY
from joint_build_database import locales, band, gig
import datetime as dt

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
                print ('Added unprintable show')
            i.dateadded = t
            session.add(i)
            session.commit()

    for home in places:
        showlist = grabTFLY(bandlist, home)
        for i in showlist:
            q = session.query(gig).filter(gig.date == i.date, gig.cleanname == i.cleanname)
            if q.first() == None:
                try:
                    print(("Adding {0} at {1} on {2} (from {3})".format(i.name, i.venue, i.date, 'Ticketfly')))
                except:
                    print ('Added unprintable show')
                i.dateadded = t
                session.add(i)
                session.commit()
    return