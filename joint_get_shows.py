from joint_concert_finder import grabTFLY, grab_bands_in_town
from joint_build_database import locales, band, gig
import datetime as dt
import progressbar

def direct_ticketfly(Session):
    session = Session()
    bandlist = session.query(band)
    places = session.query(locales)
    t = dt.date.today()
    for home in places:
        showlist = grabTFLY(bandlist, home)
        for i in showlist:
            q = session.query(gig).filter(gig.date == i.date, gig.cleanname == i.cleanname)
            if q.first() == None:
                try:
                    print(("Adding {0} at {1} on {2} (from {3})".format(i.name, i.venue, i.date, 'Ticketfly')))
                except:
                    print ('Added unprintable show from Ticketfly')
                i.dateadded = t
                session.add(i)
                session.commit()
    return

def direct_bands_in_town(Session):
    session = Session()
    bandlist = session.query(band)
    places = session.query(locales)
    t = dt.date.today()

    barmax = bandlist.count() + 1
    count = 0
    print ('Fetching Bandsintown data.')
    bandfails = []
    bandsuccesses = []
    with progressbar.ProgressBar(max_value=barmax, redirect_stdout=True) as bar:
        for bandname in bandlist:
            got_show_for_band = False
            showlist = grab_bands_in_town(bandname, places, count)
            if showlist is not None:
                for k in showlist:
                    q = session.query(gig).filter(gig.date == k.date, gig.cleanname == k.cleanname)
                    if q.first() == None:
                        try:
                            print("Adding {0} at {1} on {2} (from {3})".format(k.name, k.venue, k.date, 'Bandsintown'))
                        except:
                            print ('Added unprintable show from Bandsintown')
                        k.dateadded = t
                        got_show_for_band = True
                        session.add(k)
                        session.commit()
                    else:
                        print ("Already had {0} at {1} on {2} (from {3})".format(k.name, k.venue, k.date, 'Bandsintown'))
                        got_show_for_band = True
                if got_show_for_band == True:
                    bandsuccesses.append(bandname.cleanname)
            if not got_show_for_band:
                bandfails.append(bandname.cleanname)
            print ('Bandsuccesses: {0}      Bandfails: {1}'.format(len(bandsuccesses), len(bandfails)))
            count += 1
            bar.update(count)

    print ('Bandsuccesses: {0}      Bandfails: {1}'.format(len(bandsuccesses), len(bandfails)))

    return


def gettheshows(Session):

    #direct_ticketfly(Session)
    direct_bands_in_town(Session)
    return


