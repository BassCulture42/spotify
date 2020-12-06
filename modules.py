
import pandas as pd 
import numpy as np
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, TextInput, Button, Paragraph, Dropdown, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 

# App credentials
cid = "116761e9885b4d1eb4e5f0b076d0d7d9"
secret = "95d12cca194f425b9eaf4d5d66fced2f"
default_username = 'rubieduub'
default_playlist_id = '5ncaLdM7s3uLhn6mCPDAM7'

sp = spotipy.Spotify()
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace=False 


# ===== CUSTOMIZED FUNCTIONS FOR SPOTIFY WEB API ===== # 


# gives a list of (playlist name, playlist id) tuples
def list_playlists(username): 
    playlists = sp.user_playlists(username)
    playlist_list = []
    for playlist in playlists['items']: 
        name = playlist['name']
        playlist_list.append((name, playlist['id']))
    return playlist_list
    
    
# get a list of track, artist names for all tracks in a playlist
def getnames(username, playlist_id):
    playlist = sp.user_playlist(username, playlist_id)
    titles= []
    artists = []
    for track in playlist['tracks']['items']:
        if track['track']['id'] != None:
            title = track['track']['name']
            artist = track['track']['artists'][0]['name']
            titles.append(title)
            artists.append(artist)
    return (titles, artists)

# get a list of popularity scores for all tracks in a playlist
def getpop(username, playlist_id):
    playlist = sp.user_playlist(username, playlist_id)
    pop = []
    for track in playlist['tracks']['items']:
        if track['track']['id'] != None:
            popularity = track['track']['popularity']
            pop.append(popularity)
    return pop

# create a dataframe of all songs in a spotify playlist. contains all song features for valid tracks. 
def playlist_dataframe(username, playlist_id): 
    playlist = sp.user_playlist(username, playlist_id)
    
    songs = playlist["tracks"]["items"] 
    ids = [] 
    for i in range(len(songs)): 
        if songs[i]["track"]["id"] != None:  
            ids.append(songs[i]["track"]["id"]) 
    features = sp.audio_features(ids)     
    sdf = pd.DataFrame(features)   
    
    key_rename = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
    mode_rename = {1: 'Major', 0: 'minor'}
    sdf['key'] = sdf['key'].replace(key_rename)
    sdf['mode'] = sdf['mode'].replace(mode_rename)
    sdf['song'] = getnames(username, playlist_id)[0]
    sdf['artist'] = getnames(username, playlist_id)[1]
    sdf['popularity'] = getpop(username, playlist_id)
    return sdf

# create one object (dictionary) that contains all user playlist data
def objectify_user(username):

    data_dict = {}
    playlist_tuples = list_playlists(username)

    # create a dataframe for each playlist and add it to the object
    for p in playlist_tuples:               
        pdf = playlist_dataframe(username, p[1])
        data_dict[p[0]] = pdf
        
    # create a user object {username: object}
    user_object = {"dataframes" : data_dict}
    
    # add list of tuples to the object to use for the select widget
    user_object["playlists"] = playlist_tuples
    
    return user_object

