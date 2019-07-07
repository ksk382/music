# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import yaml
from pprint import pprint
from joint_build_database import monther, gig, band
import progressbar
from sqlalchemy import or_

def load_config():
    global user_config
    stream = open('../showtime_creds/config.yaml')
    user_config = yaml.load(stream, Loader=yaml.BaseLoader)
    #pprint(user_config)

def splog_on():
    global user_config
    load_config()
    username = user_config['username']
    print ('\n\n\n')
    print ('Logging in as username: ', user_config['username'])
    scope = 'playlist-modify-public,playlist-modify-private,user-library-read'
    token = util.prompt_for_user_token(user_config['username'],
                                       scope=scope,
                                       client_id=user_config['client_id'],
                                       client_secret=user_config['client_secret'],
                                       redirect_uri=user_config['redirect_uri'])
    if token:
        sp = spotipy.Spotify(auth=token)
        print ('Login success')
    else:
        print ("Can't get token for", user_config['username'])
    return sp, username

def find_spotify_ids(Session):
    print ('Obtaining spotify_ids')
    session = Session()
    a = session.query(band).filter(or_(
                            (band.spotify_id == None),
                            (band.spotify_id == 'failed 1'))).filter(band.song != None)
    sp, username = splog_on()
    count = 0
    barmax = a.count()
    tracksuccesses = []
    trackfails = []
    with progressbar.ProgressBar(max_value=barmax, redirect_stdout=True) as bar:
        for i in a:
            artist = i.name
            song = i.song
            if i.spotify_id == 'failed 1':
                fail_count = 1
            else:
                fail_count = 0
            id = None
            query = 'artist:{0} track:{1}'.format(artist, song)
            results = sp.search(q=query, type='track')
            if results['tracks']['total'] == 0:
                query = '{0} {1}'.format(artist, song)
                results = sp.search(q=query, type='track')
            items = results['tracks']['items']
            h = 0
            for item in items:
                if item['popularity'] > h:
                    h = item['popularity']
                    id = item['id']
            if id is not None:
                i.spotify_id = id
                print ('Spotify found:  {} - {}'.format(artist, song))
                tracksuccesses.append([artist, song])
            else:
                print ('Spotify failed: {} - {}'.format(artist, song))
                trackfails.append([artist, song])
                new_id = 'failed {}'.format(fail_count + 1)
                i.spotify_id = new_id
            session.commit()
            count +=1
            bar.update(count)
    print ('Track successes:  {0}     Track fails:      {1}'.format(len(tracksuccesses), len(trackfails)))
    return

def get_playlist_link(new_playlist_name):
    sp, username = splog_on()
    current_playlists = sp.user_playlists(username)
    match = False
    for playlist in current_playlists['items']:
        if new_playlist_name == playlist['name']:
            link = playlist['external_urls']['spotify']
            print (playlist['name'], playlist['id'], playlist['external_urls'])
            print (link)
            match = True
    if not match:
        print ('No playlist called {0} exists'.format(new_playlist_name))
        link = 'No playlist called {0} exists'.format(new_playlist_name)
    return link

def check_if_playlist_exists(sp, new_playlist_name,username):
    current_playlists = sp.user_playlists(username)
    current_playlist_names = []
    playlist_id = None
    for playlist in current_playlists['items']:
        print (playlist['name'], playlist['id'])
        current_playlist_names.append(playlist['name'])
        if new_playlist_name == playlist['name']:
            playlist_id = playlist['id']
            print ('Playlist {0} found: {1}'.format(new_playlist_name, playlist_id))
    return playlist_id

def create_playlist(sp, username, new_playlist_name):
    print ('creating playlist {0}'.format(new_playlist_name))
    playlist_id = sp.user_playlist_create(username, new_playlist_name, public=True)
    return playlist_id

def add_songs_to_playlist(sp, username, playlist_id, track_ids):
    # first get the existing contents so you are not adding duplicates
    existing_ids = []
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    i = 1
    for item in tracks:
        track = item['track']
        print ("   %d %32.32s %s     %s" % (i, track['artists'][0]['name'],
                                            track['name'], track['id']))
        existing_ids.append(track['id'])
        i +=1

    print (len(track_ids), len(existing_ids))
    ids_to_add = [x for x in track_ids if x not in existing_ids]

    print ('Total tracks checked: {0}'.format(len(track_ids)))
    print ('Pushing {0} total tracks'.format(len(ids_to_add)))
    runs = len(ids_to_add) // 99 + 1
    ids_to_add = [x for x in ids_to_add if x is not None]
    # length of a proper spotify ID is 22
    ids_to_add = [x for x in ids_to_add if len(x) == 22]

    if len(ids_to_add) > 0:
        for i in range(0, runs):
            x = (i * 99)
            y = min(((i + 1) * 99), len(ids_to_add))
            print ('Pushing tracks: {0} through {1}'.format(x, y))
            track_ids_slice = ids_to_add[x:y]
            print (track_ids_slice)
            results = sp.user_playlist_add_tracks(username, playlist_id, track_ids_slice)

def do_a_playlist(track_ids, new_playlist_name):
    sp, username = splog_on()
    playlist_id = check_if_playlist_exists(sp, new_playlist_name, username)
    if playlist_id == None:
        create_playlist(sp, username, new_playlist_name)
        print ('Created playlist {0}: {1}'.format(new_playlist_name, playlist_id))
        playlist_id = check_if_playlist_exists(sp, new_playlist_name, username)
    # delete contents of existing playlist
    #
    delete_list = []
    results = sp.user_playlist(username, playlist_id,
                               fields="tracks,next")
    tracks = results['tracks']
    print (tracks)
    for i in tracks['items']:
        delete_list.append(i['track']['id'])
    while tracks['next']:
        tracks = sp.next(tracks)
        for i in tracks['items']:
            delete_list.append(i['track']['id'])

    print ('Deleting: {0}'.format(delete_list))
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, delete_list)

    add_songs_to_playlist(sp, username, playlist_id, track_ids)
    link = get_playlist_link(new_playlist_name)
    return link

def delete_all_playlists(key_word):
    sp, username = splog_on()
    current_playlists = sp.user_playlists(username)
    for playlist in current_playlists['items']:
        x, y = playlist['name'], playlist['id']
        print (x,y)
        if key_word in x:
            f = sp.user_playlist_unfollow(username, y)
            print ('deleted {0}'.format(x))

if __name__ == "__main__":

    key_word = 'Upcoming'
    print ("Deleting all playlists with '{0}' in them".format(key_word))
    delete_all_playlists(key_word)