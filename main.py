from spotify import connect, get_playlist_id, extract_playlist_data, queries_builder
from youtube import get_vid_id, make_playlist, make_public_service, make_service, add_item_to_playlist


playlist_id = "fsdfsdf"

def main(pl_id: str): 
  api = connect()