# -*- coding: utf-8 -*-
import string
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import unicodedata
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from setup_quote_db import db, quote2
import re
import random
import datetime


engine = create_engine('sqlite:///dbQuotes2.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db)
db.metadata.create_all(engine)

session = Session()

def cleanit():
    q = session.query(quote)
    for i in q:
        i.line = i.line.strip()
        i.speaker = i.speaker.strip()
    session.commit()

def get_a_quote():
    q = session.query(quote2)
    x = [i.use_count for i in q]
    try:
        y = min(x)
        q = session.query(quote2).filter(quote2.use_count == y)
        qlist = list(q)
    except:
        qlist = [i for i in q]


    choice = random.choice(qlist)
    c = '{0} - {1}'.format(choice.line, choice.speaker)
    new_count = int(choice.use_count or 0) + 1
    choice.use_count = new_count
    date = datetime.date.today()
    choice.last_used = date
    session.commit()
    return c

if __name__ == "__main__":
    print(get_a_quote())





'''
url = 'http://www.complex.com/music/2013/04/the-50-most-outrageous-rapper-quotes/'
from selenium import webdriver


browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
browser.get(url) #navigate to the page
innerHTML = browser.execute_script("return document.body.innerHTML")

a = BeautifulSoup(innerHTML, 'html.parser')

b = a.find_all('h1')
for i in b:
    x = i.text
    y = x.split('"')
    print type(y)
    print len(y)
    if len(y) >1:
        q = y[1].strip()
        s = y[2].strip()
        while s[0] =='-':
            s = s[1:]
        print q, s
        newq = quote(line=q, speaker=s, source=url)
        ch = session.query(quote).filter(quote.line == newq.line)
        if ch.first() == None:
            print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
            session.add(newq)
        else:
            print('already had {0}'.format(newq.line))
session.commit()

'''

'''

for line in a:
    children = line.findChildren()

    for child in children:
        y = child.text
    spk = unicodedata.normalize('NFKD', y).encode('ascii', 'ignore').strip()
    x = line.find(text=True, recursive=False)
    #print x
    quo = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').strip()
    print [quo, spk]
    newq = quote(line=quo, speaker=spk, source=url)
    ch = session.query(quote).filter(line == newq.line)
    if ch.first() == None:
        print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
        session.add(newq)
    else:
        print('already had {0}'.format(newq.line))
session.commit()

'''





'''    
    y = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore')
    print y
    combo = [x.strip() for x in y.split('. ')]
    quo = combo[0] + '.'
    spk = combo[1]
    newq = quote(line = quo, speaker = spk, source = url)
    ch = session.query(quote).filter(line == newq.line)
    if ch.first() == None:
        print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
        session.add(newq)
    else:
        print('already had {0}'.format(newq.line))
session.commit()

'''

'''
    newq = quote(line = x, speaker = y, source = url)
    ch = session.query(quote).filter(line == newq.line)
    if ch.first() == None:
        print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
        session.add(newq)
    else:
        print('already had {0}'.format(newq.line))
session.commit()'''





'''
g = True
all_ = []

for x in range(0,5):
    page = x + 1
    a = []
    try:
        url = 'http://www.clashmusic.com/features/100-most-outrageous-quotes-in-music-part-' + str(page)
        print url
        r = requests.get(url)
        page = r.text
        bs = BeautifulSoup(page, "html.parser")
        a = bs.find_all('i')


    except Exception, e:
        print str(e)
        g = False
        continue

    quos = []
    spks = []


    for line in a:
        quo = line.text
        quos.append(quo)

    b = bs.find_all('strong')
    for line in b:
        if not line.text[0].isdigit():
            spk = line.text
            spks.append(spk)

    for x in range(0, len(spks)):
        cleanline = unicodedata.normalize('NFKD', quos[x]).encode('ascii', 'ignore')
        cleanspk = unicodedata.normalize('NFKD', spks[x]).encode('ascii', 'ignore')
        newq = quote(line = cleanline, speaker = cleanspk, source = url)
        ch = session.query(quote).filter(line == newq.line)
        if ch.first() == None:
            print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
            session.add(newq)
        else:
            print('already had {0}'.format(newq.line))
    session.commit()


url = 'http://www.clashmusic.com/features/50-more-rocknroll-quotes'
print url
r = requests.get(url)
page = r.text
bs = BeautifulSoup(page, "html.parser")
a = bs.find_all('center')

quotes = []
speakers = []
all_ = []

for line in a:
    b = line.text.splitlines()
    l = b
    n = 3
    c = [l[i:i+n] for i in xrange(0, len(l), n)]
    for item in c:
        gg = unicodedata.normalize('NFKD', item[1]).encode('ascii', 'ignore')
        ss = unicodedata.normalize('NFKD', item[2]).encode('ascii', 'ignore')
        newq = quote(line = gg, speaker = ss, source = url)
        ch = session.query(quote).filter(line==newq.line)
        if ch.first() == None:
            print ('Adding: \n {0} - {1}'.format(newq.line, newq.speaker))
            session.add(newq)
        else:
            print('already had {0}'.format(newq.line))
    session.commit()

'''
