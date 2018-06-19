# -*- coding: utf-8 -*-
from joint_build_database import gig, locales
from joint_music_utilities import cleanup, cleanish
import requests
import json
from geopy.distance import vincenty
import datetime as dt
import progressbar

tdelta = 60

def grabBIT(bands, places):
    print ('Fetching Bandsintown data.')
    baseURL = 'https://rest.bandsintown.com/artists/'
    foo = 'foo'
    bandfails = []
    shows = []
    tday = dt.date.today()
    b = tday + dt.timedelta(tdelta)
    count = 0
    barmax = bands.count() + 1
    j = 0
    k = list(range(4000))
    changeup = k[0::150]
    with progressbar.ProgressBar(max_value=barmax, redirect_stdout=True) as bar:
        for i in bands:
            #try:
            j = j + 1
            if j in changeup:
                foo = foo + 'o'
            cleanname = cleanish(i.name)
            urlclose = '/events?app_id=' + foo
            url = baseURL + cleanname + urlclose
            try:
                resp = requests.get(url)
                data = resp.json()
            except Exception as e:
                print((str(e)))
                print(('Error occurred while requesting band ID {0}'.format(i.id)))
                data = []
                try:
                    print(('Url was: {0}'.format(url)))
                    print(cleanname)
                    bandfails.append(cleanname)
                except:
                    print ('Unprintable name')
            if not data:
                pass
            elif data == {'errors': ['Unknown Artist']}:
                bandfails.append(cleanname)
                pass
            else:
                for show in data:
                    try:
                        venueLL = '(' + show['venue']['latitude'] + ', ' + show['venue']['longitude'] + ')'
                    except Exception as e:
                        print(str(e))
                        try:
                            print(url)
                            print((i.id))
                        except:
                            print('Unprintable: ', (i.id))
                        continue

                    for home in places:
                        try:
                            placeLL = '(' + str(home.lat) + ',' + str(home.long) + ')'
                            dist = vincenty(placeLL, venueLL).miles
                            if dist <= 20:
                                showdate = str(show['datetime'])[:10] + ' ' + str(show['datetime'])[11:19]
                                date = showdate[:10]
                                date2 = dt.datetime.strptime(date, "%Y-%m-%d").date()
                                if date2 < b:
                                    venue = show['venue']['name']
                                    city = show['venue']['city']
                                    a=gig(name = i.name.strip(), date = date, venue = venue.strip(),
                                          city = city.strip(), source = 'Bandsintown', cleanname = i.cleanname,
                                        queryby=home.sig)
                                    try:
                                        print(('Adding show: {0} - {1} {2}'.format(cleanname, a.city, a.date)))
                                    except:
                                        print ('Adding unprintable show')
                                    shows.append(a)
                        except Exception as e:
                            print(str(e))
                            try:
                                print(url)
                                print((i.id))
                            except:
                                print('Unprintable: ', (i.id))
            count +=1
            bar.update(count)
            #except Exception, e:
            #    print(str(e))
            #    try:
            #        print(cleanup(i.name))
            #    except:
            #        print 'Unprintable name'

    print(('Done fetching Bandsintown data. {0} shows grabbed.'.format(len(shows))))
    print(('Failed to find {0} bands:'.format(len(bandfails))))
    for h in bandfails:
        try:
            print (h)
        except:
            print ('unprintable band')
    return shows

def grabTFLY(bands, home):
    print(('Fetching Ticketfly concerts for {0}'.format(home.city)))
    tday = dt.date.today()
    b = tday + dt.timedelta(tdelta)
    radius = 20
    shows=[]
    baseURL = 'http://www.ticketfly.com/api/events/list.json?orgId=1'
    addlocation = '&location=geo:' + home.lat + ',' + home.long + '&distance=' + str(radius) + 'mi'
    adddates = '&fromDate=' + str(tday) + '&&thruDate=' + str(b)
    addfilters = '&fields=venue.city,startDate,venue.name,headlinersName,supportsName'
    url = baseURL + addlocation + adddates + addfilters
    print ('\n', url, '\n')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    try:
        data = resp.json()
    except:
        print ('json failed...\n\n\n')
        print(resp)
        return []
    i=1
    cleanbands = []
    for band in bands:
        cleanbands.append(band.cleanname)
    while (i <= data['totalPages']):
        newpage = '&pageNum=' + str(i)
        urlpg = url + newpage
        print (urlpg)
        resp = requests.get(urlpg, headers=headers)
        try:
            data = resp.json()
        except:
            print ('json failed...\n\n\n')
            print(resp)
        print(('Page {0} of {1}'.format(data['pageNum'], data['totalPages'])))
        barmax = len(data['events'])
        count = 0
        with progressbar.ProgressBar(max_value=barmax, redirect_stdout=True) as bar:
            for j in data['events']:
                z = cleanup(j['headlinersName'])
                y = cleanup(j['supportsName'])
                if z in cleanbands:
                    date = j['startDate'][:10]
                    venue = j['venue']['name']
                    city = j['venue']['city']
                    a = gig(name = j['headlinersName'].strip(), date = date, venue = venue.strip(),
                            city = city.strip(), source = 'Ticketfly', cleanname = z,
                            queryby=home.sig)
                    print(('Adding {0} - {1}'.format(z, a.city)))
                    shows.append(a)
                elif y in cleanbands:
                    date = j['startDate'][:10]
                    venue = j['venue']['name']
                    city = j['venue']['city']
                    a = gig(name = j['supportsName'].strip(), date = date, venue = venue.strip(),
                            city = city.strip(), source = 'Ticketfly', cleanname = y,
                            queryby=home.sig)
                    try:
                        print(('Adding {0}'.format(a.name)))
                    except:
                        print ('Added unprintable band')
                    shows.append(a)
                count += 1
                bar.update(count)
        i = data['pageNum'] + 1
    print(('{0} shows grabbed \n\n'.format(len(shows))))
    return shows