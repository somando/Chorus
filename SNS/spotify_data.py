# ------------ Import Libraries ------------
import requests
from .spotify_token import *


# Need User Data


# ------------ Get User Profile ---------------

def get_user_profile(access_token, request, headers = None):
    
    if headers == None:
        
        headers = create_header(access_token, request)
    
    response = requests.get(SPOTIFY_USER_PROFILE_URL, headers=headers).json()
    
    user = ProfileData.objects.get(user_id=request.user.id)
    
    user.spotify_id = response['id']
    
    user.spotify_premium = response['product'] == 'premium'
    
    user.save()
    
    return response


# ------------ Get Now Play Data ---------------

def get_current_play(access_token, request):
    
    headers = create_header(access_token, request)
    
    response = get_user_profile(access_token, request, headers)
    
    if response['product'] == 'premium':
        
        params = {
            'additional_types': 'track',
        }
        
        response = requests.get(SPOTIFY_CURRENT_PLAY_URL, params=params, headers=headers)
        
        if response.status_code == 204:
            
            pick_data = { 'status': { 'premium_user': True, 'playing': False, 'success': False } }
        
        else:
            
            pick_data = pick_current_play_data_from_json(response.json())
    
    else:
        
        pick_data = { 'status': { 'premium_user': False, 'playing': False, 'success': False } }
    
    return pick_data


# ------------ Get Recent Play Data ---------------

def get_recent_play(access_token, request, limit = 20):
    
    headers = create_header(access_token, request)
    
    params = {
        'limit': limit,
    }
    
    response = requests.get(SPOTIFY_RECENT_PLAY_URL, params=params, headers=headers).json()
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_RECENT_PLAY)
    
    return pick_data


# ------------ Get Saved Track Data ---------------

def get_saved_track(access_token, request):

    headers = create_header(access_token, request)
    
    params = {
        'limit': 50,
    }
    
    songs = requests.get(SPOTIFY_SAVED_TRACKS_URL, params=params, headers=headers).json()
    
    while songs['next'] != None:
        
        response = requests.get(songs['next'], headers=headers).json()
        
        songs['items'] += response['items']
        songs['next'] = response['next']
    
    pick_data = pick_song_data_from_json(songs, SPOTIFY_SAVED_TRACKS)
    
    return pick_data


# ------------ Get Saved Artist Data ---------------

def get_saved_artist(access_token, request):

    headers = create_header(access_token, request)
    
    params = {
        'limit': 50,
        'type': 'artist',
    }
    
    artists = requests.get(SPOTIFY_FOLLOW_ARTISTS_URL, params=params, headers=headers).json()
    
    while artists['artists']['next'] != None:
        
        response = requests.get(artists['artists']['next'], headers=headers).json()
        
        artists['artists']['items'] += response['artists']['items']
        artists['artists']['next'] = response['artists']['next']
    
    pick_data = pick_artist_data_from_json_for_library(artists)
    
    return pick_data


# ------------ Get Saved Album Data ---------------

def get_saved_album(access_token, request):

    headers = create_header(access_token, request)
    
    params = {
        'limit': 50,
    }
    
    albums = requests.get(SPOTIFY_SAVED_ALBUMS_URL, params=params, headers=headers).json()
    
    while albums['next'] != None:
        
        response = requests.get(albums['next'], headers=headers).json()
        
        albums['items'] += response['items']
        albums['next'] = response['next']
    
    pick_data = pick_album_data_from_json_for_library(albums)
    
    return pick_data


# ------------ Get Saved Playlist Data ---------------

def get_saved_playlist(access_token, request):

    headers = create_header(access_token, request)
    
    user = ProfileData.objects.get(user_id=request.user.id)
    
    params = {
        'limit': 50,
    }
    
    playlists = requests.get(SPOTIFY_GET_PLAYLISTS_URL + user.spotify_id + '/playlists', params=params, headers=headers).json()
    
    while playlists['next'] != None:
        
        response = requests.get(playlists['next'], headers=headers).json()
        
        playlists['items'] += response['items']
        playlists['next'] = response['next']
    
    pick_data = pick_playlist_data_from_json_for_library(playlists, user.spotify_id)
    
    return pick_data


# ------------ Get Playlist Data by ID ---------------

def search_playlist_id(playlist_id, access_token, request):
    
    if access_token == None:
        
        headers = create_header()
    
    else:
        
        headers = create_header(access_token, request)
    
    playlist_response = requests.get(SPOTIFY_SEARCH_PLAYLIST_ID_URL + playlist_id, headers=headers).json()
    
    params = {
        'limit': 50,
    }
    
    tracks_response = requests.get(SPOTIFY_SEARCH_PLAYLIST_ID_URL + playlist_id + '/tracks', params=params, headers=headers).json()
    
    while tracks_response['next'] != None:
        
        params = {
            'limit': 50,
            'offset': len(tracks_response['items']),
        }
        
        response = requests.get(SPOTIFY_SEARCH_PLAYLIST_ID_URL + playlist_id + '/tracks', params=params, headers=headers).json()
        
        tracks_response['items'] += response['items']
        tracks_response['next'] = response['next']
    
    pick_data = pick_playlist_data_from_json(playlist_response, tracks_response)
    
    return pick_data


def get_queue(access_token, request):
    
    headers = create_header(access_token, request)
    
    response = requests.get(SPOTIFY_QUEUE_URL, headers=headers).json()
    
    return response


def control(method, access_token, request):
    
    headers = create_header(access_token, request)
    
    if method == 'play':
        
        requests.put(SPOTIFY_CONTROL_START_URL, headers=headers)
    
    elif method == 'pause':
        
        requests.put(SPOTIFY_CONTROL_PAUSE_URL, headers=headers)
    
    elif method == 'next':
        
        requests.post(SPOTIFY_CONTROL_NEXT_URL, headers=headers)
    
    elif method == 'previous':
        
        requests.post(SPOTIFY_CONTROL_PREVIOUS_URL, headers=headers)


# No Need User Data

# ------------ Search for Query ---------------

def search_query(type, query, limit = 20, offset = 0):

    headers = create_header()
    
    search_params = {
        'q': query,
        'type': type,
        'limit': limit,
        'offset': offset,
    }
    
    response = requests.get(SPOTIFY_SEARCH_TEXT_URL, params=search_params, headers=headers).json()
    
    if type == SPOTIFY_SEARCH_TYPE_TRACK:
        
        pick_data = pick_song_data_from_json(response, SPOTIFY_SEARCH_FOR_ITEM)
    
    else:
        
        pick_data = pick_any_data_from_json(response)
    
    return pick_data


# ------------ Search for Track & Artist ---------------

def search_track_artist(type, track = None, artist = None, limit = 20, offset = 0):
    
    query = ""
    
    if artist != None:
        query = 'artist:' + artist + ' '
    
    if track != None:
        query += 'track:' + track
    
    return search_query(type, query, limit, offset)


# ------------ Search for Track by ID ---------------

def search_track_id(track_id, lang='ja'):

    headers = create_header(lang=lang)
    
    response = requests.get(SPOTIFY_SEARCH_TRACK_ID_URL + track_id, headers=headers).json()
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_GET_TRACK)
    
    return pick_data


# ------------ Get Album Data by ID ---------------

def search_album_id(album_id):

    headers = create_header()
    
    params = {
        'limit': 50,
    }
    
    album_response = requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id, params=params, headers=headers).json()
    
    get_tracks = album_response['total_tracks']
    
    track_response = requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id + '/tracks', params=params, headers=headers).json()
    
    while len(track_response['items']) < get_tracks:
        
        track_params = {
            'limit': '50',
            'offset': len(track_response['items']),
        }
        
        track_response['items'] += requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id + '/tracks', params=track_params, headers=headers).json()['items']
    
    pick_data = pick_album_data_from_json(album_response, track_response)
    
    return pick_data


# ------------ Get Artist Data by ID ---------------

def search_artist_id(artist_id):

    headers = create_header()
    
    artist_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id, headers=headers).json()
    
    track_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/top-tracks', headers=headers).json()
    
    params = {
        'include_groups': 'album,single,appears_on,compilation',
        'limit': 50,
    }
    
    album_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/albums', params=params, headers=headers).json()
    
    while album_response['next'] != None:
        
        params = {
            'include_groups': 'album,single,appears_on,compilation',
            'limit': 50,
            'offset': len(album_response['items']),
        }
        
        response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/albums', params=params, headers=headers).json()
        
        album_response['items'] += response['items']
        album_response['next'] = response['next']
    
    pick_data = pick_artist_data_from_json(album_response, artist_response, track_response)
    
    return pick_data
