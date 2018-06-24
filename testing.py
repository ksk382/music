
# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from joint_build_database import band
from pytz import timezone
import re
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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



if __name__ == "__main__":

    x = sgum(50)
    for i in x:
        print (i.name, i.appeared, i.album)
    print (len(x))
    #x = metacritic(50)
    #for i in x:
    #    print (i.name)
