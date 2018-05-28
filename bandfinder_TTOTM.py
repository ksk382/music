# -*- coding: utf-8 -*-
from joint_build_database import band
from gsheetpull import sheetpull
from joint_music_utilities import cleanup
from joint_get_bands import get_TTOTM_bands
import datetime as dt

def getthebands(Session):
    session = Session()
    session.query(band).delete()
    bandlist = get_TTOTM_bands()
    today = dt.date.today()
    errs = []
    for item in bandlist:
        bandname = item[0].strip()
        try:
            z = cleanup(item[0])
            addtrack = band(name=bandname, song=item[1].strip(), appeared=item[2].strip(), cleanname = z,
                            dateadded = today, source = 'Master List')
            q = session.query(band).filter(band.name == addtrack.name)
            if q.first() == None:
                session.add(addtrack)
            session.commit()
        except Exception as e:
            print(str(e))
            print('(while in getthebands() loop)')
            errs.append(addtrack.name)

    print('Done adding TTOTM bands to the database.')
    print(('Errors: {0}'.format(len(errs))))
    return




