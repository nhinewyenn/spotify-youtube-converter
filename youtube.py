from googleapiclient.discovery import build
from credentials import yt_api


def make_public_service(api_key: str):
    service = build(serviceName="youtube", version="v3", developerKey="api key here")
    return service