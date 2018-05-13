from gmusicapi import Mobileclient
from music.nonTTOTM.shred import shredlists
from collections import defaultdict
import re
import progressbar
from shutil import copyfile
import os
import unicodedata
import sys
import json

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
playlist_name = 'scout'

def gettracks(artistId):
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
        existing_tracks = get_existing_tracks()
        for b in reversed(recentalbum):
            for track in topsongs:
                if track['album'] == b['name']:
                    if track['nid'] not in addsongs and track['nid'] not in existing_tracks:
                        if len(addsongs) < 3:
                            addsongs.append(track['nid'])
    except Exception as e:
        print(str(e))
        print('inside getracks(), lines 33-41')

    return addsongs

def loadsongs(addsongs):
    playlist_id = get_id()
    if len(addsongs) > 1:
        try:
            api.add_songs_to_playlist(playlist_id, addsongs)
        except Exception as e:
            print('Couldnt add to playlist')
            print(str(e))
    else:
        print ('Already got this track.')
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

def remove_stale():
    allcontents = api.get_all_user_playlist_contents()
    for i in allcontents:
        if i['name'] == 'Scout':
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



if __name__ == "__main__":

    #copy the bands database from the TTOTM folder
    print('\n\n\nFirst you need to fix the directory....\n\n\n')

    src = os.getcwd() + '/../TTOTM/bandsdb.db'
    dst = os.getcwd() + '/bandsdb.db'
    print("Copying {0} to {1}\n".format(src, dst))
    copyfile(src, dst)

    allcontents = api.get_all_user_playlist_contents()

    exists = False
    for i in allcontents:
        if i['name']== playlist_name:
            exists = True
            scout = i
            playlist_id = scout['id']
            existing_tracks = scout['tracks']

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

    #getthebands()
    # 9/4: should replace this function with the joint_music_utilities function...requires passing a Session object
    bandlist = shredlists()

    print(('Checking {0} bands'.format(len(bandlist))))

    misses = []
    count = 0
    with progressbar.ProgressBar(max_value=len(bandlist), redirect_stdout=True) as bar:
        for band in bandlist:
            printable = False
            try:
                print(('Trying {0}'.format(band)))
                printable = True
            except:
                print ('Unprintable band.')
            if printable == True:
                if existing_bands[band] < 3:
                    query = str(band)
                    results1 = api.search(query, max_results=50)
                    try:
                        cleanname = cleanup(results1['artist_hits'][0]['artist']['name'])
                    except Exception as e:
                        print(str(e))
                        try:
                            print(results1['artist_hits'][0])
                        except:
                            pass
                        cleanname = ''
                    cleanq = cleanup(query)
                    if cleanq == cleanname:
                        artistId = results1['artist_hits'][0]['artist']['artistId']
                        addsongs = gettracks(artistId)
                        loadsongs(addsongs)
                    else:
                        print(('Did not easily find {0}'.format(band)))
                else:
                    print(('Already have {0} from {1}'.format(existing_bands[band], band)))
            count = count + 1
            bar.update(count)

    print ('Done')
    print(('Missed {0} bands: {1}'.format(len(misses)), misses))

    removed_artists = remove_stale()
    print(('Removed the following bands: \n {0}'.format(removed_artists)))
