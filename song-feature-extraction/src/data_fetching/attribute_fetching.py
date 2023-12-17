import requests
from ..auth import SpotifyAuth

from pprint import pprint


def get_tracks_attributes(tracks_ids: list[str], credentials: SpotifyAuth) -> list[dict[str, int | str]]:
    """
    Fetches a dictionary mapping a `track_id` to a dictionary of track attributes like `speechiness` etc.
    """
    # Define list to store results of several iterations
    track_attributes = []

    # NOTE: API restricts us to 100 ids at a time
    CHUNK_SIZE = 100
    # NOTE: So we chunk the incoming track_ids to chunks of 100
    chunked_track_ids: list[list[str]] = [tracks_ids[idx: idx + CHUNK_SIZE] for idx in range(0, len(tracks_ids), CHUNK_SIZE)]

    # Pre-reqs for calling API
    TARGET_URL = "https://api.spotify.com/v1/audio-features"
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }
    # Call API for each sublist
    for i, chunk in enumerate(chunked_track_ids):
        print(f"Fetching chunk {i} using the following ids: {chunk}")

        PARAMS = {
            'ids': ",".join(chunk)
        }

        # Make request
        response = requests.get(
            url=TARGET_URL,
            headers=HEADERS,
            params=PARAMS
        )

        # Get response content
        response_content = response.json()["audio_features"]

        # Add it to our result list
        track_attributes.extend(response_content)

    return tracks_ids







