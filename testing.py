
# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from joint_build_database import band
from pytz import timezone
from selenium import webdriver
import socket

def metacritic(maxbands):

    url = 'http://www.metacritic.com/browse/albums/score/metascore/year/filtered'
    socket.setdefaulttimeout(15)

    try:
        browser = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    except:
        try:
            browser = webdriver.Firefox()  # replace with .Firefox(), or with the browser of your choice
        except:
            print ('Metacritic failed. Returning nothing')
            return []

    browser.get(url)  # navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML")

    bs = BeautifulSoup(innerHTML, 'html.parser')

    allbands = []

    a = bs.find('div', {'class': 'product_rows'})
    b = a.find_all('div', {'class': 'product_row release'})
    for i in b:
        artist = i.find('div', {'class': 'product_item product_artist'}).text.strip()
        album = i.find('div', {'class': 'product_item product_title'}).text.strip()
        newband = band(name=artist, appeared='Metacritic', album = album)
        allbands.append(newband)

    browser.quit()

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


if __name__ == "__main__":
    
    metacritic(50)