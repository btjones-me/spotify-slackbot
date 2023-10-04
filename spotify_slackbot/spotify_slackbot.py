"""Run slackbot."""

import slack_sdk
import requests
import dotenv
import os
import re

from spotify_slackbot.helpers import (
    extract_spotify_links,
    get_spotify_token,
    get_track_uris_from_album,
    add_tracks_to_playlist,
)


dotenv.load_dotenv()

SLACK_CLIENT_SECRET = os.getenv("SLACK_BOT_USER_OATH_TOKEN")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_BEARER_TOKEN = os.getenv("SPOTIFY_BEARER_TOKEN")


# Initialize Slack API
client = slack_sdk.WebClient(token=SLACK_CLIENT_SECRET)

# Initialize Spotify API
# spotify_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
headers = {"Authorization": f"Bearer {SPOTIFY_BEARER_TOKEN}"}

# Fetch Slack channel history
channel_id = "C05ULAS02CF"  # "test-slackbot"
client.conversations_info(channel=channel_id)
response = client.conversations_history(channel=channel_id)
messages = response["messages"]

# Find Spotify links
spotify_links = [extract_spotify_links(m["text"]) for m in messages]
spotify_links = [x for x in spotify_links if x != []]  # Remove empty lists

# Initialize an empty list to store all track URIs
all_track_uris = []

# Extract Spotify URIs from Slack messages and get track URIs
for link in spotify_links:
    link = link[0]  # Extract the first link
    id_ = link.split("/")[-1]
    if "track" in link:
        all_track_uris.append(f"spotify:track:{id_}")
    elif "album" in link:
        all_track_uris.extend(get_track_uris_from_album(id_, headers))
    else:
        print(f"Unknown link type: {link}")

# Create a new Spotify playlist
playlist_data = {
    "name": "Slack Channel Playlist",
    "description": "Created from Slack channel links",
    "public": False,
}
playlist_response = requests.post(
    "https://api.spotify.com/v1/me/playlists", headers=headers, json=playlist_data
)
playlist_id = playlist_response.json()["id"]

# Add all track URIs to the new Spotify playlist
add_tracks_to_playlist(all_track_uris, playlist_id, headers)
