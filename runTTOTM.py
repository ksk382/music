# -*- coding: utf-8 -*-
from bandfinder_TTOTM import getthebands
from joint_get_shows import gettheshows
import socket
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database import db, band
from joint_people_and_places import identify_people, identify_places
from joint_notify import notify
import sys
from joint_spotify_work import find_spotify_ids

socket.setdefaulttimeout(15)
# creation of the SQL database and the "session" object that is used to manage
# communications with the database
engine = create_engine('sqlite:///../databases/dbTTOTM.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

metadata = MetaData(db)
db.metadata.create_all(engine)

session = Session()
ttotm = 'TTOTM'
json_name = '../showtime_creds/ajsonmlist.json'

def estereo(Session):
    session = Session()
    a = session.query(band).filter(band.cleanname == 'bombaestereo')
    for i in a:
        i.comment = 'Aw hell yeah this is gonna be such a tight show'
    return

if __name__ == "__main__":

    try:
        if sys.argv[1] == 'live':
            live_mode = True
            print ('Running live.')
        else:
            live_mode = False
            print ('Running in test.')
    except:
        print ('Running in test.')
        live_mode = False

    identify_people(Session, json_name)
    identify_places(Session)
    getthebands(Session)
    gettheshows(Session)
    find_spotify_ids(Session)
    estereo(Session)
    notify(Session, ttotm, live_mode=live_mode)