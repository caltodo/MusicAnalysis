import os
import base64
from urllib.parse import urlencode
import requests
import re

# Set environment variables

os.environ['SPOTIPY_CLIENT_ID'] = 'c24c5f113ae54900b2d00ff68db31733'
os.environ['SPOTIPY_CLIENT_SECRET'] = '8095c6f50e1b424eba66ba3e5089285a'

# Get environment variables
USER = os.getenv('SPOTIPY_CLIENT_ID')
PASSWORD = os.environ.get('SPOTIPY_CLIENT_SECRET')

client_creds = f"{USER}:{PASSWORD}"
client_creds_b64 = base64.b64encode(client_creds.encode())

#Set up token
token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "client_credentials"
}
token_header = {
    "Authorization": f"Basic {client_creds_b64.decode()}" #base64 encoded
}


r = requests.post(token_url, data=token_data, headers=token_header)
token_response_data = r.json()
access_token = token_response_data['access_token']
header = {
    "Authorization": f"Bearer {access_token}"
}

#Function Definition

#GetVariation
#Pass in two dataframes (target, library)
#Populate variation between frame 1 and 2 in a new column
def GetVariation(targ, lib):
    print("Getting Variation")
    print(lib['Danceability'][0])
    l = len(lib)
    var_list = []
    for i in range(l):
        var_list.append(abs((lib['popularity'][i] - targ['popularity']) + (lib['Danceability'][i] - targ['Danceability']) + (lib['Energy'][i] - targ['Energy']) + (lib['Loudness'][i] - targ['Loudness']) + (lib['Speechiness'][i] - targ['Speechiness']) + (lib['Acousticness'][i] - targ['Acousticness']) + (lib['Instrumentalness'][i] - targ['Instrumentalness']) + (lib['Liveness'][i] - targ['Liveness']) + (lib['Tempo'][i] - targ['Tempo'])))

    lib['Variation'] = var_list
    return lib

#GetIDs
#Pre-conditions: pass in dataframe of songs (with at least 'Name')
#Post-conditions: Populate dataframes with Spotify Data = {id, popularity}
def GetIDs(df):
   l = len(df)
   endpoint = "https://api.spotify.com/v1/search"

   id_list = []
   pop_list = []

   for i in range(l):
      #print(i)
      song_name = df['Name'][i]
    
      #song_name = test_list['Name'][i]
      #print(song_name)
      data = urlencode({"q": song_name, "type": "track"}) #I need it to search for song name + artist name
      lookup_url = f"{endpoint}?{data}"
      r = requests.get(lookup_url, headers = header)
      #print(r.status_code)
      results = r.json()
      items = results['tracks']['items']
      id_list.append(items[0]['id'])
      pop_list.append(items[0]['popularity'])

   df['id'] = id_list
   df['popularity'] = pop_list
   return df

#GetData
#Pre-conditions: pass in dataframe with spotify id's
#Post-conditions: Populate dataframe with data = {Danceability, Energy, Loudness, etc...}
def GetData(df):
    l = len(df)
    endpoint = "https://api.spotify.com/v1/audio-features/"

    dance_list = []
    energy_list = []
    loud_list = []
    speech_list = []
    acoustic_list = []
    instrument_list = []
    live_list = []
    tempo_list = []

    for i in range(l):
        #print(df['Name'][i])
        s_id = df['id'][i]
        lookup_url = f"{endpoint}{s_id}"
        r2 = requests.get(lookup_url, headers = header)
        song_info = r2.json()
        dance_list.append(song_info['danceability'])
        energy_list.append(song_info['energy'])
        loud_list.append(song_info['loudness'])
        speech_list.append(song_info['speechiness'])
        acoustic_list.append(song_info['acousticness'])
        instrument_list.append(song_info['instrumentalness'])
        live_list.append(song_info['liveness'])
        tempo_list.append(song_info['tempo'])

    df['Danceability'] = dance_list
    df['Energy'] = energy_list
    df['Loudness'] = loud_list
    df['Speechiness'] = speech_list
    df['Acousticness'] = acoustic_list
    df['Instrumentalness'] = instrument_list
    df['Liveness'] = live_list
    df['Tempo'] = tempo_list
    return df

def CleanPar(df):
    names = df['Name'].tolist()
    items = []
    for item in names:
        items.append(re.sub(r" ?\([^)]+\)", "", item))

    df['Name'] = items
    return df

def CleanBrack(df):
    names = df['Name'].tolist()
    items = []
    for item in names:
        items.append(re.sub(r" ?\[[^)]+\]", "", item))

    df['Name'] = items
    return df

def CleanSlash(df):
    names = df['Name'].tolist()
    items = []
    sep = '/'
    for item in names:
        items.append(item.split(sep, 1)[0])

    df['Name'] = items
    return df

def CleanDupes(df):
    df.drop_duplicates(subset ="Name", keep = "first", inplace = True)
    #Reset index for looping                     
    df.reset_index(drop=True, inplace=True)
    return df

def CrossRef(playlist, library):
    cond = playlist['Name'].isin(library['Name'])
    library.drop(library[cond].index, inplace = True)
    return library
