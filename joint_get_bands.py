# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from joint_build_database import band
from pytz import timezone
import socket
from selenium import webdriver
import re
from random import shuffle

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
                album = banddiv.findNext("h2").text
                newband = band(name=banddiv.text, appeared='Pitchfork 8.0+ reviews', album = album)
                allbands.append(newband)
        except Exception as e:
            print (str(e))
            print(("Page {0} failed".format(i)))
            continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def pfork_tracks(maxbands):
    c = []
    allbands = []
    i = 0
    while (len(allbands) < maxbands) and (i < 50):
        i = i + 1
        try:
            print(('Pitchfork page: {0}'.format(i)))
            site = 'https://pitchfork.com/reviews/tracks/?page=' + str(i)
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(site, headers=hdr)
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            a = soup.findAll("div", {"class": "track-collection-item__details"})
            print(("Page {0} retrieved".format(i)))
            for banddiv in a:
                artist = banddiv.find('ul', {'class': 'artist-list'}).li.text \
                    .strip().replace('”', '').replace('“', '')
                track = banddiv.find('h2', {'class': 'track-collection-item__title'}).text \
                    .strip().replace('”', '').replace('“', '')
                print (artist, track)
                newband = band(name=artist, appeared='Pitchfork Top Tracks',
                               song=track)
                allbands.append(newband)
        except Exception as e:
            print (str(e))
            print(("Page {0} failed".format(i)))
            continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]

def MTM(maxbands):

    url = 'http://feeds.kexp.org/kexp/musicthatmatters'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    allbands = []
    maxbands = 200
    c = []

    for item in bs.findAll('item'):
        if len(allbands) <= maxbands:
            desc = item.find('description').text
            tr = False
            s = ''
            n = []

            for g in range(0, len(desc)):
                if desc[g].isdigit():
                    if desc[g + 1].isdigit() or desc[g + 1] == '.':
                        tr = False
                        if len(s) > 0:
                            n.append(s)
                        s = ''
                if desc[g] == '.':
                    if desc[g - 1].isdigit():
                        tr = True
                if tr == True:
                    s = s + desc[g]

            for i in n:
                h = i[2:].strip().split('<')[0]
                egg = h.split('-')
                if len(egg) < 2:
                    egg = h.split('–')
                if len(egg) < 2:
                    egg = h.split('-')

                try:
                    artist = egg[0].strip()
                    song = egg[1].strip()
                    newband = band(name=artist, appeared='KEXP Music That Matters',
                                   song=song)
                    allbands.append(newband)
                except Exception as e:
                    print (str(e))
                    try:
                        print (h)
                    except:
                        print('unprintable')
                    continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def metacritic(maxbands):

    socket.setdefaulttimeout(15)
    url = 'http://www.metacritic.com/browse/albums/score/metascore/year/filtered'

    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get(url)

    innerHTML = driver.execute_script("return document.body.innerHTML")
    bs = BeautifulSoup(innerHTML, 'html.parser')

    driver.quit()
    allbands = []

    a = bs.find('div', {'class': 'product_rows'})
    b = a.find_all('div', {'class': 'product_row release'})
    for i in b:
        artist = i.find('div', {'class': 'product_item product_artist'}).text.strip()
        album = i.find('div', {'class': 'product_item product_title'}).text.strip()
        newband = band(name=artist, appeared='Metacritic', album = album)
        allbands.append(newband)

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def sgum(maxbands):

    socket.setdefaulttimeout(10)
    allbands = []
    url1 = 'https://www.stereogum.com/category/franchises/album-of-the-week/'

    j = 1
    while len(allbands) < maxbands:
        print ('Getting Stereogum Album of the Week, page {0}'.format(j))
        url = url1 + 'page/' + str(j) + '/'

        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get(url)

        innerHTML = driver.execute_script("return document.body.innerHTML")
        bs = BeautifulSoup(innerHTML, 'html.parser')

        driver.quit()

        a = bs.find_all('h2')
        for i in a:
            if 'Album Of The Week:' in i.text:
                b = re.sub('Album Of The Week:', '', i.text)
                c = i.find('em')
                if c == None:
                    c = i.find('i')
                album = c.text.strip()
                artist = re.sub(album, '', b).strip()
                newband = band(name=artist, appeared='Stereogum', album=album)
                allbands.append(newband)

        j+=1
        print ('Found {0} bands so far'.format(len(allbands)))

    c = []
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
                parens = d[1].find('(')
                album = d[1][:parens]
            d = e.split('–')
            if len(d) == 2:
                artist = d[0].strip()
                parens = d[1].find('(')
                album = d[1][:parens].strip()

            print (artist, album)
            newband = band(name=artist, appeared = genre, album = album)
            allbands.append(newband)

    # half of this list will be the Top 90
    d = []
    e = []
    for i in allbands:
        if i.appeared == 'KEXP Top 90':
            if i not in d:
                d.append(i)
        else:
            if i not in e:
                e.append(i)

    half = maxbands // 2
    d = d[:half]
    shuffle(e)
    c = d + e[half:maxbands]

    return c[:maxbands]

def KEXP_harvest(maxbands):

    socket.setdefaulttimeout(5)

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
            except Exception as e:
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

    socket.setdefaulttimeout(15)

    return c


def KCRW_harvest(maxbands):
    c = []
    i = 1
    allbands = []
    print ('Grabbing KCRW bands')
    while (i<20) and len(allbands)<maxbands:
        url = 'https://tracklist-api.kcrw.com/Simulcast/all/' + str(i)
        response = urllib.request.urlopen(url).read()
        data = json.loads(response)
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

