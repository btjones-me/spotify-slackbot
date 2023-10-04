import re
import base64
import requests
import json


def extract_spotify_links(message):
    # Regular expression pattern to match Spotify album and track URLs
    pattern = r"(https://open\.spotify\.com/(album|track)/[a-zA-Z0-9?=.]+)"

    # Find all matching URLs
    return [match[0] for match in re.findall(pattern, message)]


def get_spotify_token(client_id, client_secret):
    # Encode credentials
    credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")
    ).decode("utf-8")

    # Get access token
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {credentials}"},
        data={"grant_type": "client_credentials"},
    )

    # Parse JSON response
    token_info = json.loads(response.text)
    access_token = token_info["access_token"]

    # use like
    # headers = {"Authorization": f"Bearer {access_token}"}

    return access_token


def get_track_uris_from_album(album_id, headers):
    """Fetch all track URIs in an album."""
    track_uris = []
    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks", headers=headers
    )
    response.raise_for_status()
    album_data = response.json()
    for track in album_data["items"]:
        track_uris.append(track["uri"])
    return track_uris


def add_tracks_to_playlist(track_uris, playlist_id, headers):
    """Add a list of track URIs to a Spotify playlist."""
    requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": track_uris},
    )
