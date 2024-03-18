from spotify import connect, get_playlist_id, extract_playlist_data, queries_builder
from youtube import get_vid_id, make_playlist, make_public_service, make_service, add_item_to_playlist
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()
client_id = os.getenv("SP_CLIENT_ID")
if client_id is None:
    logging.error("SP_CLIENT_ID is not set in the environment variables.")
    raise ValueError("SP_CLIENT_ID is not set in the environment variables.")

client_secret = os.getenv("SP_CLIENT_SECRET")
if client_secret is None:
    logging.error("SP_CLIENT_SECRET is not set in the environment variables.")
    raise ValueError("SP_CLIENT_SECRET is not set in the environment variables.")

yt_key = os.getenv("YT_API_KEY")
if yt_key is None:
    logging.error("YT_API_KEY is not set in the environment variables.")
    raise ValueError("YT_API_KEY is not set in the environment variables.")



playlist_id = "add id here"

def main(pl_id: str): 
  try:
        # Connect to Spotify API and get playlist
        api = connect(client_id, client_secret)
        items_name = get_playlist_id(api, pl_id)
        if not items_name:
            logging.error(f"Failed to fetch playlist data for playlist ID: {pl_id}")
            return None

        playlist_name = items_name[1]
        queries = queries_builder(extract_playlist_data(api, items_name[0]))

        # Get YouTube video IDs
        vid_ids = get_vid_id(queries, yt_key)
        if not vid_ids:
            logging.warning("No video IDs were found.")
            return None

        # Create new YouTube playlist
        service = make_service()
        new_pl_id = make_playlist(service, playlist_name)
        if not new_pl_id:
            logging.error("Failed to create a new YouTube playlist.")
            return None

        # Add videos to the new YouTube playlist
        success = add_item_to_playlist(service, new_pl_id, vid_ids)
        if not success:
            logging.error("Failed to add videos to the new YouTube playlist.")
            return None

        logging.info("Finished migrating playlist.")
        return new_pl_id

  except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

print(main(playlist_id))