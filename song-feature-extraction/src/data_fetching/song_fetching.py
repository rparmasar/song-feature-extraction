import requests
from ..auth import SpotifyAuth
from ..data_types import Track, Artist
from pprint import pprint
# TODO: Convert this to return a Track
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


def get_playlist_tracks(playlist_id: str, credentials: SpotifyAuth) -> list[Track]:
    """
    Returns a dictionary of all tracks with track name, track id and artists for the track.
    """
    # Define list to hold our intermediate results
    track_list = []

    # Variable to keep track of if we've fetched all the data
    HAS_PAGES_TO_FETCH = True

    # Initial variables
    TARGET_URL = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }
    PARAMS = {
        'market': 'US',
        'fields': 'next,limit,offset,items(track(name,id,type,artists(id,name)))',
        'offset': 0,
        'limit': 100
    }

    while HAS_PAGES_TO_FETCH:
        # Make request
        response = requests.get(
            url=TARGET_URL,
            headers=HEADERS,
            params=PARAMS
        )

        # Get response content
        # print(f"Fetching from {response.url=}")
        response_content = response.json()

        # Add it to the intermediate list
        track_list.extend(response_content['items'])

        # Check if we still need to fetch
        if response_content['next'] is None:
            HAS_PAGES_TO_FETCH = False
        else:
            PARAMS['offset'] = response_content['limit'] + PARAMS['offset'] + 1
            
    # Convert output to Track objs
    def _create_track(track_obj: dict[str, dict[str, str] | str]) -> Track:
        artists = [Artist(**art) for art in track_obj['artists']]
        
        track = Track(
            id=track_obj["id"],
            name=track_obj["name"],
            artists=artists,
        )

        return track

    # We need to ignore episode types
    tracks = [_create_track(track["track"]) for track in track_list if track["track"]["type"] == 'track']

    return tracks

        


        

    
    

