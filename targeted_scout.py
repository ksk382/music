from gmusicapi import Mobileclient
from collections import defaultdict
import re
import progressbar
from shutil import copyfile
import os
import unicodedata
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database import band, db
from bandfinder_NT import getthebands
from joint_music_utilities import shredTTOTMs
import pickle as pickle

engine = create_engine('sqlite:///dbNonTTOTM.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

metadata = MetaData(db)
db.metadata.create_all(engine)

api = Mobileclient()
hidden_vals = '../showtime_creds/ajsonhidden_vals.json'
try:
    jfile = open(hidden_vals)
except:
    print('Need a file named ajsonhidden_vals.json in the current working directory with login information.')
    sys.exit()

jstr = jfile.read()
jdata = json.loads(jstr)
gaccount = jdata['Gmusic login']['account']
gapi = jdata['Gmusic login']['api_key']
api.login(gaccount, gapi, Mobileclient.FROM_MAC_ADDRESS)
# => True

print(api.is_authenticated())

def gettracks(artistId, existing_nids):
    recentalbum = []
    try:
        results = api.get_artist_info(artistId, include_albums=True,
                                       max_top_tracks=20, max_rel_artist=5)
        albums = results['albums']
        for a in albums:
            if (str(a['year']) == '2017'):
                recentalbum.append(a)
    except Exception as e:
        print('Couldnt get an album')
        print(str(e))

    addsongs = []
    try:
        topsongs = results['topTracks']
        for b in reversed(recentalbum):
            for track in topsongs:
                if track['album'] == b['name']:
                    if track['nid'] not in addsongs and track['nid'] not in existing_nids:
                        if len(addsongs) < 3:
                            addsongs.append(track['nid'])
    except Exception as e:
        print(str(e))
        print('inside getracks(), lines 33-41')

    return addsongs

def loadsongs(addsongs):
    playlist_id = get_id()
    try:
        api.add_songs_to_playlist(playlist_id, addsongs)
    except Exception as e:
        print('Couldnt add to playlist')
        print(str(e))
    return

def cleanup(name):
    name = name.lower().encode('utf-8')
    name = name.decode('utf-8')
    name = ''.join(c for c in unicodedata.normalize('NFKD', name) if unicodedata.category(c) != 'Mn')
    name = name.encode('utf-8')
    badwords = ['and ', 'the ', '& ']
    for word in badwords:
        name = re.sub(word, '', name)
    name = ''.join(e for e in name if e.isalnum())
    return name

def remove_stale(playlist_id):
    allcontents = api.get_all_user_playlist_contents()
    for i in allcontents:
        if i['id'] == playlist_id:
            if len(i['tracks']) > 100:
                # making sure it's the right Scout playlist
                scout = i
                tracks = scout['tracks']

    removals = []
    removed_artists = []
    for j in tracks:
        try:
            if j['track']['playCount'] > 3:
                print(("Removing {0} - {1}".format(j['track']['artist'], j['track']['title'])))
                removals.append(j['id'])
                removed_artists.append(j['track']['artist'])
        except:
            print(j['track']['artist'], 'no playcount', '\n')

    api.remove_entries_from_playlist(removals)
    return removed_artists

def get_id():
    allcontents = api.get_all_user_playlist_contents()
    playlist_name = 'scout'

    exists = False
    for i in allcontents:
        if i['name'] == playlist_name:
            playlist_id = i['id']
            exists = True

    if exists == False:
        print(('Creating playlist {0}'.format(playlist_name)))
        playlist_id = api.create_playlist(playlist_name, description=None, public=False)
        print(('Playlist ID: {0}'.format(playlist_id)))

    return playlist_id


def get_existing_tracks():
    existing_tracks = []
    for i in allcontents:
        if i['name'] == playlist_name:
            existing_tracks = i['tracks']
    return existing_tracks

def get_the_bands():
    getthebands(Session)


def clean_the_db():
    shredTTOTMs(Session)
    pass

def remove_repeats(playlist_name):


    api.remove_entries_from_playlist(removals)
    return removed_artists

if __name__ == "__main__":

    get_the_bands()
    clean_the_db()
    session = Session()
    bandlist = session.query(band)
    print('First count: {0}'.format(bandlist.count()))


    # Going to run this without any Pitchfork review bands or Jazz Theater bands
    bandlist = session.query(band).filter(band.source != 'Pitchfork')
    print('Without Pitchfork: {0}'.format(bandlist.count()))
    bandlist = bandlist.filter(band.appeared != 'KEXP Jazz Theater')
    print('Without Jazz Theater: {0}'.format(bandlist.count()))
    j = bandlist
    bandlist = []
    for i in j:
        if int(i.dateadded[5:7]) > 10:
            bandlist.append(i)
    print('Oct and after: {0}'.format(len(bandlist)))


    allcontents = api.get_all_user_playlist_contents()
    playlist_name = 'scout'

    exists = False
    existing_tracks = []
    exists = False
    delete_old = False

    for i in allcontents:
        if i['name'] == playlist_name:
            playlist_id = i['id']
            if delete_old == True:
                print(('Deleting old playlist {0}'.format(playlist_name)))
                print(('Playlist ID: {0}'.format(playlist_id)))
                api.delete_playlist(playlist_id)
            else:
                exists = True
                existing_tracks = i['tracks']

    if exists == False:
        print(('Creating playlist {0}'.format(playlist_name)))
        playlist_id = api.create_playlist(playlist_name, description=None, public=False)
        print(('Playlist ID: {0}'.format(playlist_id)))
        existing_tracks = []

    if exists == False:
        print(('Creating playlist {0}'.format(playlist_name)))
        playlist_id = api.create_playlist(playlist_name, description=None, public=False)
        print(('Playlist ID: {0}'.format(playlist_id)))
        existing_tracks = []

    existing_nids = []
    existing_bands = defaultdict(int)
    for j in existing_tracks:
        existing_nids.append(j['track']['nid'])
        bandonlist = j['track']['artist']
        existing_bands[bandonlist] += 1



    #print('Removing repeats')
    #remove_repeats(playlist_name) this needs more work




    print(('Checking {0} bands'.format(len(bandlist))))

    misses = []
    totalsongs = []
    count = 0

    with progressbar.ProgressBar(max_value=len(bandlist), redirect_stdout=True) as bar:
        for item in bandlist:
            band = item.name
            printable = False
            try:
                print(('Trying {0}'.format(band)))
                printable = True
            except:
                print ('Unprintable band.')
            if printable == True:
                if existing_bands[band] < 1:
                    query = str(band)
                    results1 = api.search(query, max_results=50)
                    try:
                        cleanname = cleanup(results1['artist_hits'][0]['artist']['name'])
                    except Exception as e:
                        print(str(e))
                        try:
                            print(results1['artist_hits'][0])
                        except:
                            misses.append(band)
                            pass
                        cleanname = ''
                    cleanq = cleanup(query)
                    if cleanq == cleanname:
                        artistId = results1['artist_hits'][0]['artist']['artistId']
                        addsongs = gettracks(artistId, existing_nids)
                        addsongs = [i for i in addsongs if i not in existing_nids]
                        totalsongs = totalsongs + addsongs
                    else:
                        print(('Did not easily find {0}'.format(band)))
                        misses.append(band)
                else:
                    print(('Already have {0} from {1}'.format(existing_bands[band], band)))
            count = count + 1
            bar.update(count)

    print(('Adding tracks to playlist {0}'.format(playlist_name)))
    try:
        loadsongs(totalsongs)
    except:
        pickle.dump(totalsongs, open('totalsongs.p', 'wb'))
    print ('Done')
    print(('Missed {0} bands: {1}'.format(len(misses), misses)))

    removed_artists = remove_stale(playlist_id)
    print(('Removed the following bands: \n {0}'.format(removed_artists)))
