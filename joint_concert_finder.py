# -*- coding: utf-8 -*-
from joint_build_database import gig, locales
from joint_music_utilities import cleanup, cleanish
import requests
import json
from geopy.distance import vincenty
import datetime as dt
import progressbar
import urllib

tdelta = 60

def grab_bands_in_town(bandname, places, count):

    baseURL = 'https://rest.bandsintown.com/artists/'
    bandfails = []
    shows = []
    tday = dt.date.today()
    b = tday + dt.timedelta(tdelta)
    foo_count = count // 200
    foo = 'yoo' + foo_count * 'o'
    i = bandname
    cleanname = cleanish(i.name)
    urlclose = '/events?app_id=' + foo
    cleanname_url = urllib.parse.quote_plus(cleanname)
    url = baseURL + cleanname_url + urlclose

    data = False
    venueLL = 0

    try:
        resp = requests.get(url)
        data = resp.json()
        if not data:
            cleanname_url = urllib.parse.quote(cleanname)
            url = baseURL + cleanname_url + urlclose
            resp = requests.get(url)
            data = resp.json()
    except Exception as e:
        print ('Error occurred while requesting band ID {0}:'.format(i.id))
        print (str(e))
        data = []
        try:
            print(('Url was: {0}'.format(url)))
            print(cleanname)
            bandfails.append(cleanname)
        except:
            print ('Unprintable name')

    if not data:
        print ('No data for {0}     {1}'.format(cleanname, url))
        return None
    elif data == {'errors': ['Unknown Artist']}:
        print ('Unknown artist for {0}      {1}'.format(cleanname, url))
        return None
    else:
        for show in data:
            try:
                venueLL = '(' + show['venue']['latitude'] + ', ' + show['venue']['longitude'] + ')'
            except Exception as e:
                print ('Inside the for show in data loop: {0}'.format(str(e)))
                try:
                    if str(e) == "'latitude'":
                        print (show['venue'])
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
                            a = gig(name=i.name.strip(), date=date, venue=venue.strip(),
                                    city=city.strip(), source='Bandsintown', cleanname=i.cleanname,
                                    queryby=home.sig)
                            shows.append(a)

                except Exception as e:
                    print(str(e))
                    try:
                        print(url)
                        print((i.id))
                    except:
                        print('Unprintable: ', (i.id))
    return shows

def grabTFLY(bands, home):
    print(('Fetching Ticketfly concerts for {0}'.format(home.city)))
    tday = dt.date.today()
    b = tday + dt.timedelta(tdelta)
    radius = 20
    shows=[]
    bandsuccesses = []
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
                    print('Adding {0} - {1}'.format(z, a.city))
                    shows.append(a)
                    if z not in bandsuccesses:
                        bandsuccesses.append(z)
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
                    if y not in bandsuccesses:
                        bandsuccesses.append(z)
                count += 1
                bar.update(count)
        i = data['pageNum'] + 1
    print ('{0} shows grabbed \n\n'.format(len(shows)))
    bandfails = list(set(cleanbands) - set(bandsuccesses))
    print ('Bandsuccesses: {0}      Bandfails: {1}'.format(len(bandsuccesses), len(bandfails)))
    return shows