import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from typing import Optional, Tuple, List, Dict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
client_id = os.getenv("SP_CLIENT_ID")
client_secret = os.getenv("SP_CLIENT_SECRET")

if not client_id:
    logging.error("SP_CLIENT_ID is not set in the environment variables.")
    raise ValueError("SP_CLIENT_ID is not set in the environment variables.")

if not client_secret:
    logging.error("SP_CLIENT_SECRET is not set in the environment variables.")
    raise ValueError("SP_CLIENT_SECRET is not set in the environment variables.")


# Establish connection with spotify api using spotipy
def connect(cl_id: str, cl_secret: str) -> Optional[spotipy.Spotify]:
    try:
        auth_manager = SpotifyClientCredentials(client_id=cl_id, client_secret=cl_secret)
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return spotify
    except Exception as e:
        logging.error(f"Error connecting to Spotify API: {e}")
        return None
   
# Fetch playlist details
def get_playlist_id(api: spotipy.Spotify, id: str) -> Tuple[Optional[List], Optional[str]]:
    try:
        playlist = api.playlist(playlist_id=id)
        name = playlist["name"]
        playlist_items = playlist["tracks"]["items"]
        return playlist_items, name
    except Exception as e:
        logging.error(f"Error fetching playlist: {e}")
        return None, None
    



# Extract name, artists, album name
def extract_playlist_data(api, track_items: List)  -> List[Dict]:  
    """
    Returns: List[Dict]: A list of dictionaries containing track data.
    """
    
    tracks_data = []  
    for i in track_items:
        try:
            track_name = i['track']['name']
            artist_name = i["track"]["artists"][0]["name"]
            album_name = i["track"]["album"]["name"]
            track_data = {
                'track_name': track_name,
                'artist_name': artist_name,
                'album_name': album_name
            }
            tracks_data.append(track_data)
        except Exception as e:
            logging.error(f"Error extracting track data: {e}")
    return tracks_data
    
# Queries to search on youtube
def queries_builder(playlist_data):
    queries = []
    for obj in playlist_data:
        # Construct a query string using track_name, album_name, and artist_name
        query = f"{obj['track_name']} {obj['album_name']} {obj['artist_name']}"
        queries.append(query)
    return queries


# TEST
# pl_id="your id"
# api = connect(client_id, client_secret)
# pl = get_playlist_id(api, pl_id)
# print("playlist data")
# print(json.dumps(pl))
# print("queries")
# print(queries_builder(extract_playlist_data(api,pl[0])))