# music
A program for findings concerts based on bands favored by the music sharing group, TTOTM

There are three main files that run the whole project: 
  1. runTTOTM.py, which collects TTOTM bands, finds the shows, and emails TTOTM members by city.
  2. runNonTTOTM.py, which collects bands from a couple different sources like radio DJs and music review sites, and also finds shows and emails a couple people who wanted to be on that list.
  3. runAll.py, which does the work of both the previous files and puts them into one email, which is sent to a couple of people who wanted to be on that list.
  
  
  
While the TTOTM stuff requires access to the TTOTM Google Sheet, anyone can run the nonTTOTM program. It needs a few things prior to running though:

1. You need a create a directory adjacent to your working directory called 'showtime_creds/' to store credentials in. For example, if you're running this program out of 'docs/music/showtime', you need a directory called docs/music/showtime_creds'.
    -In that directory, create a .json file named 'ajsonnonmlist.json', and add recipient information to it in the following format, where radius is how far they want to travel to see a show:
              {
                "Kevin DC": {
                  "email": "kevinsemail@gmail.com",
                  "city": "Washington",
                  "state": "DC",
                  "radius": "20"
                }
              }
              
    -Also in the showtime_creds/ directory, you need to create another json that stores login information from the sending email address (which will send out the shows to the recipient). This should just look like this (needs to be a gmail account, otherwise you need to change the code in joint_notify.py in the send_email() function):
              {
                "dev email": {
                  "email": "youremail@gmail.com"
                }
              }

2. You might need to install several packages that are used in the program:
  -Python 2
  -SQLAlchemy, since everything is stored in SQL using SQL Alchmey Object Relational Mapping 
        $ pip install SQLAlchemy
  -Beautiful Soup 4 (bs4), which helps parse HTML
        $ pip install beautifulsoup4
  -oathtools, which is part of google's api python client library
        $ pip install --upgrade google-api-python-client 
  -geopy, which enables measurement of geographic distances
        $ pip install geopy
        
3. Then, run with 
        $ python runNonTTOTM.py
