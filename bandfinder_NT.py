from joint_get_bands import Pitchfork_charts, KCRW_harvest, \
    KEXP_charts, load_kexp_bands, metacritic, sgum, pfork_tracks, \
    MTM
import datetime as dt
from joint_music_utilities import cleandb, cleanup, shredTTOTMs
from joint_build_database import band

bandsources = ['KCRW', 'KEXP Music That Matters', 'Pitchfork Top Tracks',
               'Stereogum', 'Metacritic', 'KEXP playlists',
               'Pitchfork', 'KEXP charts']

def getthebands(Session):
    # this loop pulls down band names from the sources identified.
    # each source, however, needs its own function, since the
    # websites are set up differently
    session = Session()
    today = dt.date.today()
    for src in bandsources:
        print(src)
        list = grabbands(src)
        for i in list:
            h = cleanup(i.name)
            if h != '':
                try:
                    q = session.query(band).filter(band.cleanname == h)
                    if q.first() == None:
                        i.source = src
                        i.cleanname = h
                        i.dateadded = today
                        #newband = i(name=i, source=src, cleanname=h, dateadded=today)
                        print(("Adding {0} (from {1})".format(i.name, i.source)))
                        session.add(i)
                        session.commit()
                except Exception as e:
                    print(str(e))
    cleandb(Session)
    a = shredTTOTMs(Session)
    print(('Deleted {0} TTOTM bands'.format(a)))
    return

def grabbands(src):
    maxbands = 100
    if src == 'Pitchfork':
        maxbands = 50
        list = Pitchfork_charts(maxbands)
    if src == 'KEXP charts':
        maxbands = 150
        list = KEXP_charts(maxbands)
    if src == 'KCRW':
        list = KCRW_harvest(maxbands)
    if src == 'KEXP playlists':
        list = load_kexp_bands(maxbands)
    if src == 'Metacritic':
        try:
            list = metacritic(maxbands)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'Stereogum':
        try:
            list = sgum(maxbands)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'Pitchfork Top Tracks':
        try:
            list = pfork_tracks(200)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'KEXP Music That Matters':
        try:
            list = MTM(200)
        except Exception as e:
            list = []
            print (str(e))
            pass
    return list

if __name__ == "__main__":

    print ('Getting bands')
    getthebands()
    print ('Done getting bands')









