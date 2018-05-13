from gsheetpull import sheetpull
import urllib.request, urllib.parse, urllib.error, json
import datetime as dt
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from joint_build_database import band


maxbands = 45
c = []
allbands = []

basesite = 'http://kexp.org/charts/'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(basesite, headers=hdr)
page = urllib.request.urlopen(req)
bs = BeautifulSoup(page, "html.parser")


for row in bs.findAll('p', {'class': 'paragraph'}):
    if row.b:
        genre = row.b.text.strip(':')
        print (genre)
    elif row.text == []:
        print ('here')
        continue
    elif len(row.text) > 1:
        a = row.text
        b = a.split()
        if b[0][0].isdigit():
            b.remove(b[0])
        c = ' '.join(i for i in b)
        c = c.replace('(self-released)', '')
        #print (c)
        d = c.split('-')
        if len(d) == 2:
            artist = d[0]
        d = c.split('–')
        if len(d) == 2:
            artist = d[0]

        print (artist)




#print (c[:maxbands])