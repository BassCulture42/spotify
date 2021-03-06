from modules import playlist_dataframe, list_playlists, objectify_user

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource, HoverTool, TextInput, Button, Paragraph, Dropdown, Select
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

output_notebook()

import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 



# App credentials
cid = "###################################"
secret = "################################"

sp = spotipy.Spotify()
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace=False 

username = "rubieduub"
user_object = objectify_user(username)
