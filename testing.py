# -*- coding: utf-8 -*-
from bandfinder_All import getthebands
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
engine = create_engine('sqlite:///../databases/dbAll.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

metadata = MetaData(db)
db.metadata.create_all(engine)

find_spotify_ids(Session)