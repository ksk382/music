# -*- coding: utf-8 -*-
import datetime as dt
import unicodedata
import re
from gsheetpull import sheetpull
from joint_build_database import gig, band

def cleandb(Session):
    session = Session()
    # kill of shows that have passed or are not within 60 days
    allshows = session.query(gig).order_by(gig.date.asc())
    today = dt.datetime.today()
    tdelta = 60
    twomonths = today + dt.timedelta(tdelta)
    for show in allshows:
        a = dt.datetime.strptime(show.date, '%Y-%m-%d')
        if (a < today) or (a > twomonths):
            session.delete(show)
            session.commit()
    return

def shredTTOTMs(Session):
    TTOTMlist = sheetpull()
    session = Session()
    delete_count = 0
    for tband in TTOTMlist:
        name = cleanup(tband[0])
        bands = session.query(band).filter(band.cleanname == name)
        gigs = session.query(gig).filter(gig.cleanname == name)
        for i in bands:
            session.delete(i)
            session.commit()
            delete_count += 1
        for i in gigs:
            session.delete(i)
            session.commit()
    return delete_count

def cleanup(name):
    #this one strips spaces
    name = cleanish(name)
    cleanname = ''.join(e for e in name if e.isalnum())
    return cleanname

def cleanish(name):
    #this one leaves in the spaces
    #name = name.encode('utf-8')
    badwords = ['and ', 'the ', 'The ', '& ', '’', 'w/ ', '/']
    for word in badwords:
        name = re.sub(word, '', name)
    c = name
    #name = str(c.decode('utf-8'))
    cleanishname = ''.join(c for c in unicodedata.normalize('NFKD', name) if unicodedata.category(c) != 'Mn')
    cleanname = cleanishname.lower().rstrip().lstrip()
    return cleanname
