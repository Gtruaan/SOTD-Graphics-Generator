"""
All logic for requesting song info and cover
"""
import requests
from requests.exceptions import HTTPError
import spotipy
import json


with open("spotify-credentials.json", "r") as f:
    client_info = json.load(f)

username = client_info["username"]
client_id = client_info["client_id"]
client_secret = client_info["client_secret"]
redirect_uri = client_info["redirect_uri"]
scope = "user-read-recently-played"


token = spotipy.util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=client_id,
                                           client_secret=client_secret,
                                           redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)


def getTrackID(track_name: str) -> str:
    headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
              "Authorization": f"Bearer {token}",
              }
    params = [
             ("q", track_name),
             ("type", "track"),
             ]
    try:
        response = requests.get("https://api.spotify.com/v1/search",
                                headers=headers, params=params)
        json = response.json()

        if not len(json["tracks"]["items"]):
            return None

        first_result = json["tracks"]["items"][0]
        track_id = first_result["id"]

        return track_id
    except HTTPError:
        return None


def getTrackInfo(id: str) -> dict:
    return sp.track(id)


def getTrackAttributes(track_name: str) -> tuple:
    id = getTrackID(track_name)

    if id is None:
        return None

    info = getTrackInfo(id)

    image_url = info["album"]["images"][0]["url"]
    track_name = info["name"]
    artist_name = info["artists"][0]["name"]

    return image_url, track_name, artist_name
