# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database import band
from setup_quote_db import quote, quote2

#grab bands from the other two databases
#databases = ['sqlite:///dbNonTTOTM.db', 'sqlite:///dbNonTTOTM copy.db']
databases = ['sqlite:///dbQuotes.db', 'sqlite:///dbQuotes2.db']

engines = []
sessions = []
for dbconninfo in databases:
    engine = create_engine(dbconninfo)
    engines.append(engine)
    sessions.append(sessionmaker(bind=engine)())

def copy_music():

    a = sessions[1].query(band)

    for j in a:
        newobj = band(name=j.name, song=j.song, appeared=j.appeared,
                      cleanname=j.cleanname, source=j.source, dateadded=j.dateadded)
        q = session[0].query(band).filter(band.cleanname == newobj.cleanname)
        if q.first() == None:
            session[0].add(newobj)
        session[0].commit()

    b = sessions[1].query(gig)

    for k in b:
        newg = gig(
            name = j.name,
            cleanname = j.cleanname,
            date = j.date,
            venue = j.venue,
            city = j.city,
            source = j.city,
            queryby = j.queryby,
            dateadded = j.dateadded
        )
        q = session[0].query(gig).filter(gig.cleanname == newg.cleanname, gig.queryby == newg.queryby, gig.date == newg.date)
        if q.first() == None:
            session[0].add(newobj)
        session[0].commit()

def copy_quotes():
    a = sessions[0].query(quote)
    for j in a:
        newobj = quote2(id=j.id, line=j.line, speaker=j.speaker, source=j.source)
        q = sessions[1].query(quote2).filter(quote2.line == newobj.line)
        if q.first() == None:
            sessions[1].add(newobj)
            print('added {0}'.format(newobj.speaker))
        sessions[1].commit()

if __name__ == "__main__":
    copy_quotes()
