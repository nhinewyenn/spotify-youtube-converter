import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import json
from typing import Optional, Tuple, List, Dict

load_dotenv()
client_id = os.getenv("SP_CLIENT_ID")
client_secret = os.getenv("SP_CLIENT_SECRET")


# Establish connection with spotify api using spotipy
def connect(cl_id: str, cl_secret: str) -> spotipy.Spotify:
    auth_manager = SpotifyClientCredentials(client_id=cl_id, client_secret=cl_secret)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify
   
# Fetch playlist details
def fetch_playlist_id(api: spotipy.Spotify, id: str) -> Tuple[Optional[List], Optional[str]]:
    try:
        playlist_resp = api.playlist(playlist_id=id)
        name = playlist_resp["name"]
        playlist_items = playlist_resp["tracks"]["items"]
        return playlist_items, name
    except Exception as error:
        print("Error fetching playlist:", error)
        return None, None
    
pl_id="3zdRAg3wGmcjOkQp2D6JTH"

api = connect(client_id, client_secret)
playlist_items = fetch_playlist_id(api, pl_id)
print(json.dumps(playlist_items))


# Extract name, artists, album name
def extract_playlist_data(api, track_items: List)  -> List[Dict]:  
    """
    Returns:
        List[Dict]: A list of dictionaries containing track data.
    """
    
    tracks_data = []
    
    for i in track_items: 
        track_name = i['track']['name']
        artist_name = i["track"]["artists"][0]["name"]
        album_name = i["track"]["album"]["name"]
        
        track_data = {
            'track_name': track_name,
            'artist_name': artist_name,
            'album_name': album_name
        }
     
        tracks_data.append(track_data)
        print(tracks_data)
        return tracks_data
    
# Queries to search on youtube
def queries_builder(playlist_data):
    queries = []
    for obj in playlist_data:
        # Construct a query string using track_name, album_name, and artist_name
        query = f"{obj['track_name']} {obj['album_name']} {obj['artist_name']}"
        queries.append(query)
    return queries