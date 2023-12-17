import requests
from ..auth import SpotifyAuth

from pprint import pprint

def get_artist_tracks(artist_id: str, credentials: SpotifyAuth) -> dict[str, str]:
    """
    Returns a dictionary of the top songs for a given artist (Maxes at 10).
    """
    # Define endpoint
    TARGET_URL = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'

    # Include token in header
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }

    # Send request
    response = requests.get(
        url=TARGET_URL,
        headers=HEADERS
    )

    tracks = response.json()["tracks"]

    parsed_content = {track["name"]: track["id"] for track in tracks}

    return parsed_content


def get_playlist_tracks(playlist_id: str, credentials: SpotifyAuth) -> list[dict[str, str | dict[str, str]]]:
    """
    Returns a dictionary of all tracks with track name, track id and artists for the track.
    """
    # Define list to hold our intermediate results
    track_list = []

    # Variable to keep track of if we've fetched all the data
    HAS_PAGES_TO_FETCH = True

    # Initial variables
    TARGET_URL = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }
    PARAMS = {
        'market': 'US',
        # 'fields': 'tracks%28next%2Citems%28track%28name%2Cid%2Cartists%28id%2Cname%29%29%29'
        # 'fields': 'tracks(next,items(track(name,id,artists(id,name)))'
        'fields': 'tracks(next,items(track(name,id,artists(id,name))))'
    }

    while HAS_PAGES_TO_FETCH:
        # Make request
        response = requests.get(
            url=TARGET_URL,
            headers=HEADERS,
            params=PARAMS
        )

        # Get response content
        response_content = response.json()['tracks']

        # Add it to the intermediate list
        track_list.extend(response_content['items'])

        # Check if we still need to fetch
        if response_content['next'] is None:
            HAS_PAGES_TO_FETCH = False
        else:
            HAS_PAGES_TO_FETCH = True

    return track_list

        


        

    
    

