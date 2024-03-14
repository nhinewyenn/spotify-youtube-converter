from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import List
import os

def make_public_service(api_key: str):
    service = build(serviceName="youtube", version="v3", developerKey=api_key)
    return service

def get_vid_id(queries: List[str], api: str) -> List[str]:
    service = make_public_service(api)
    ids = []
    for query in queries:
        req = service.search().list(part="snippet", maxResults=1, q=query)
        res = req.execute()
        vid_id = res['items'][0]['id']['videoId']
        print(vid_id)
        
        ids.append(vid_id)
        time.sleep(3)
    return ids
    
# Create service object to interact with youtube api
def make_service() -> build:
    credentials = None

    # Load client secrets from file
    client_secret_file = "client_secret.json"
    if os.path.exists(client_secret_file):
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file,
            scopes=["https://www.googleapis.com/auth/youtube"]
        )
        credentials = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
    
    service = build(serviceName="youtube", version="v3", credentials=credentials)
    return service

def make_playlist(service, name):
    """
     Args:
        service: A Google service object used to interact with the Google API.
        name: A string representing the name of the playlist to be created.
    """
    
    playlist = {
        "snippet": {
            "title": name
        }
    }

    req = service.playlists().insert(
        part="snippet",
        body=playlist
    )

    res = req.execute()
    return res['id']

def add_item_to_playlist(service, playlist_id, items):
    res = []
    for i in items:
        req = service.playlistItems().insert(
             part="snippet",
            body={
                "snippet": {
                    "playlistId": str(playlist_id),
                    "resourceId": {"kind": "youtube#video", "videoId": i},
                }
            },
        )
        response = req.execute()
        print("ADDED")
        res.append(response)
    return res 