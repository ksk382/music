
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





if __name__ == "__main__":

    x = KCRW_harvest(50)
    for i in x:
        print (i.name, i.appeared, i.album)
    print (len(x))

