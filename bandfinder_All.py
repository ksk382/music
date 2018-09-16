# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from joint_build_database import band

#grab bands from the other two databases
databases = ['sqlite:///../databases/dbNonTTOTM.db', 'sqlite:///../databases/dbTTOTM.db']

engines = []
sessions = []
for dbconninfo in databases:
    engine = create_engine(dbconninfo)
    engines.append(engine)
    sessions.append(sessionmaker(bind=engine)())

def getthebands(sss):
    aa = []
    bb = []
    print (band)
    a = sessions[0].query(band)
    for i in a:
        aa.append(i)

    b = sessions[1].query(band)
    for i in b:
        bb.append(i)

    cc = aa + bb
    print ('Adding bands from both TTOTM and non-TTOTM databases')
    for j in cc:
        newobj = band(name = j.name, song = j.song, appeared = j.appeared,
                      cleanname = j.cleanname, source = j.source, dateadded = j.dateadded)
        q = sss.query(band).filter(band.cleanname == newobj.cleanname)
        if q.first() == None:
            sss.add(newobj)
        sss.commit()

if __name__ == "__main__":
    dd = merge_lists()
    for i in dd:
        print(i.cleanname, i.source)
    print(len(dd))
