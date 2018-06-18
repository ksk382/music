# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, urllib.parse, urllib.error, json, getopt
import datetime as dt
import urllib
from bs4 import BeautifulSoup
from joint_build_database import band
from pytz import timezone

def get_TTOTM_bands():
    TTOTMbands = sheetpull()
    print(('{0} total TTOTM tracks'.format(len(TTOTMbands))))
    return TTOTMbands

def Pitchfork_charts(maxbands):
    c = []
    allbands = []
    i=0
    while (len(allbands) < maxbands) and (i<20):
        i = i+1
        try:
            print(('Pitchfork page: {0}'.format(i)))
            site = 'http://pitchfork.com/reviews/best/albums/?page=' + str(i)
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(site, headers=hdr)
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            a = soup.findAll("ul", {"class": "artist-list"})
            print(("Page {0} retrieved".format(i)))
            for banddiv in a:
                newband = band(name=banddiv.text, appeared='Pitchfork 8.0+ reviews')
                allbands.append(newband)
        except:
            print(("Page {0} failed".format(i)))
            continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def KEXP_charts(maxbands):

    allbands = []

    basesite = 'http://kexp.org/charts/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(basesite, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    for row in bs.findAll('p', {'class': 'paragraph'}):
        if row.b:
            genre = 'KEXP ' + row.b.text.strip(':')
            print (genre)
        elif row.text == []:
            print ('empty')
            continue
        elif len(row.text) > 1:
            a = row.text
            b = a.split()
            if b[0][0].isdigit():
                b.remove(b[0])
            e = ' '.join(i for i in b)
            e = e.replace('(self-released)', '')
            # print (c)
            d = e.split('-')
            if len(d) == 2:
                artist = d[0]
            d = e.split('–')
            if len(d) == 2:
                artist = d[0]

            print (artist)
            newband = band(name=artist, appeared = genre)
            allbands.append(newband)

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)
    return c[:maxbands]


def KEXP_harvest(maxbands):

    shows = {
        'Swingin Doors': {'day': '3', 'time': '18:00', 'duration': 3},
        'Roadhouse': {'day': '2', 'time': '18:00', 'duration': 3},
        'DJ Riz': {'day': '0', 'time': '21:00', 'duration': 3},
        'Street Sounds': {'day': '6', 'time': '18:00', 'duration': 3},
        'El Toro': {'day': '2', 'time': '21:00', 'duration': 3},
        'Jazz Theater': {'day': '0', 'time': '01:00', 'duration': 2},
        'Sonic Reducer': {'day': '5', 'time': '21:00', 'duration': 3},
        'Troy Nelson': {'day': '5', 'time': '15:00', 'duration': 3}
    }

    today = dt.date.today()
    alltracks = []
    allbands = []

    i = 0
    for show in shows:
        found_at = show
        allshowfinds = []
        while len(allshowfinds) < maxbands and i < 20:
            showbands = []
            offset = (today.weekday() - int(shows[show]['day'])) % 7 + (i * 7)
            showday = today - dt.timedelta(days=offset)
            showtime = shows[show]['time'] + ':00'
            combined = str(showday) + ' ' + showtime
            seattletime = dt.datetime.strptime(combined, '%Y-%m-%d %H:%M:%S')

            # This is in Pacific US timezone
            ptime = timezone('US/Pacific')
            seattletime = ptime.localize(seattletime)

            # Convert to UTC
            utc = timezone('UTC')
            starttime = seattletime.astimezone(utc)

            duration = shows[show]['duration']
            endtime = starttime + dt.timedelta(hours=(duration))
            startstring = dt.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S') + 'Z'
            endstring = dt.datetime.strftime(endtime, '%Y-%m-%dT%H:%M:%S') + 'Z'

            print ('\n\n\n\n')
            print (startstring)
            print (endstring)

            endtime = starttime + dt.timedelta(hours=(duration))
            startstring = dt.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S') + 'Z'
            endstring = dt.datetime.strftime(endtime, '%Y-%m-%dT%H:%M:%S') + 'Z'
            url = 'https://legacy-api.kexp.org/play/?limit=200&start_time={0}&end_time={1}&ordering=-airdate'. \
                format(startstring, endstring)
            # https://legacy-api.kexp.org/play/?limit=200&start_time=2017-08-10T23:00:00&end_time=2017-08-11T02:00:00&ordering=-airdate
            print('{3}. Grabbing bands from the KEXP {2} playlist: {0} to {1}'.format(startstring, endstring, show, i))
            print (url)
            print ('\n')
            try:
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                dump = data['results']
            except getopt.GetoptError as e:
                print (str(e), '\n')
                dump = []

            # print json.dumps(data, indent=4, sort_keys=True)
            for item in dump:
                a = item['airdate']
                # 2018-03-30T01:00:00Z
                b = a[:10] + ' ' + a[11:-1]
                # '2017-08-10 16:35:00'
                c = dt.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
                c = utc.localize(c)
                s = starttime
                if c > s:
                    try:
                        if item is None:
                            continue
                        if item['artist'] is None:
                            continue
                        if item['track'] is None:
                            continue
                        newband = band(name=item['artist']['name'], song=item['track']['name'], appeared=found_at)
                        showbands.append(newband)
                    except Exception as e:
                        print((str(e)))
                        print('\n')
                        pass
            bandlist = [k.name for k in showbands]
            print (bandlist)
            allshowfinds = allshowfinds + showbands
            i = i+1
        allbands = allbands + allshowfinds

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)
    return c




def KCRW_harvest(maxbands):
    c = []
    i = 1
    allbands = []
    print ('Grabbing KCRW bands')
    while (i<20) and len(allbands)<maxbands:
        url = 'https://tracklist-api.kcrw.com/Simulcast/all/' + str(i)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        print(("KCRW page {0} \n".format(i)))
        for entry in data:
            bandname = entry["artist"]
            trackname = entry['title']
            if bandname != "[BREAK]":
                newband = band(name=bandname, song=trackname, appeared = 'KCRW')
                allbands.append(newband)
        i+=1

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]

