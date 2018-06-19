from joint_get_bands import Pitchfork_charts, KCRW_harvest, KEXP_charts, KEXP_harvest, metacritic
import datetime as dt
from joint_music_utilities import cleandb, cleanup, shredTTOTMs
from joint_build_database import band

maxbands = 200
bandsources = ['KEXP playlists', 'Pitchfork', 'KEXP charts', 'Metacritic', 'KCRW']

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
    maxbands = 75
    if src == 'Pitchfork':
        list = Pitchfork_charts(maxbands)
    if src == 'KEXP charts':
        list = KEXP_charts(maxbands)
    if src == 'KCRW':
        list = KCRW_harvest(maxbands)
    if src == 'KEXP playlists':
        list = KEXP_harvest(maxbands)
    if src == 'Metacritic':
        list = metacritic(maxbands)
    return list

if __name__ == "__main__":

    print ('Getting bands')
    getthebands()
    print ('Done getting bands')









