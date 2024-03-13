from googleapiclient.discovery import build
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv("") # we need to put the api key from the .env file here




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
    
    
def make_service():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube"],)