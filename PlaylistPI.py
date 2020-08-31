#Playlist PI
#Author: Calvin Todorovich

#Setting up libraries and environment
import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
import datetime
from datetime import datetime,date #for cleaning the dates
import matplotlib.pyplot as plt
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
from urllib.parse import urlencode
import requests
import re

import PlaylistPI_functions as PI



def main():
    print("Welcome to Playlist PI")

    print("Loading Data")
    #In the future, prompt the user to browse files for playlist
    playlist_df = pd.read_csv('STCD_data.csv', low_memory=False)
    #library_df = pd.read_csv('MusicLibrary3.csv', low_memory=False, encoding='latin1')
    library_df = pd.read_csv('top_plays.csv', low_memory=False, encoding = 'latin1')  #Has ~400 songs, should be much faster

    print("Cleaning Data")    
    library_df = PI.CleanPar(library_df)
    playlist_df = PI.CleanPar(playlist_df)

    library_df = PI.CleanBrack(library_df)
    playlist_df = PI.CleanBrack(playlist_df)

    library_df = PI.CleanSlash(library_df)
    playlist_df = PI.CleanSlash(playlist_df)

    library_df = PI.CleanDupes(library_df)
    playlist_df = PI.CleanDupes(playlist_df)

    library_df.fillna(0, inplace=True)
    playlist_df.fillna(0, inplace=True)

    print("Getting Spotify Data")
    playlist_df = PI.GetIDs(playlist_df)
    library_df = PI.GetIDs(library_df)

    playlist_df = PI.GetData(playlist_df)
    library_df = PI.GetData(library_df)

    target = playlist_df.mean()

    library_df = PI.GetVariation(target, library_df)
    print("Result: ")
    print(library_df.sort_values(by='Variation').head(15)) #Lowest Variation => Most similar to target


if __name__ == "__main__":
    main()