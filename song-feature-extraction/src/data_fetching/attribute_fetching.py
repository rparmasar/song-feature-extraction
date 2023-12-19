import requests
from pandas import unique

from ..auth import SpotifyAuth

from ..data_types import TrackAttributes, TrackMetaData, Artist, Track


def get_tracks_attributes(tracks_ids: list[str], credentials: SpotifyAuth) -> list[TrackAttributes]:
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
        print(f"[track_attributes] Fetching chunk {i} with {len(chunk)} IDs ...")

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
        
        # Convert to TrackAttribute Objects
        track_attributes_objs = [
            TrackAttributes(**{key: val for (key,val) in track_attrs.items() if key in TrackAttributes.__dataclass_fields__}) 
            for track_attrs in response_content
            if track_attrs is not None
        ]

        # Add it to our result list
        track_attributes.extend(track_attributes_objs)

    return track_attributes


def get_tracks_metadata(tracks_ids: list[str], credentials: SpotifyAuth) -> list[TrackMetaData]:
    """
    Returns a list of `TrackMetaData` which keeps track of the release date and the track's popularity.
    """
    # Define list to store results of several iterations
    track_metadata = []

    # NOTE: API restricts us to 50 ids at a time
    CHUNK_SIZE = 50
    # NOTE: So we chunk the incoming track_ids to chunks of 100
    chunked_track_ids: list[list[str]] = [tracks_ids[idx: idx + CHUNK_SIZE] for idx in range(0, len(tracks_ids), CHUNK_SIZE)]

    # Pre-reqs for calling API
    TARGET_URL = "https://api.spotify.com/v1/tracks"
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }
    
    # Call API for each sublist
    for i, chunk in enumerate(chunked_track_ids):
        print(f"[track_metadata] Fetching chunk {i} with {len(chunk)} IDs ...")

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
        response_content = response.json()["tracks"]
        
        # Convert to TrackMetaData Objects
        for track_obj in response_content:
            # Move to next iteration if None
            if track_obj is None:
                continue

            # NOTE: Our release date metrics are tied to the album sub-field
            current_track_metadata = TrackMetaData(
                id = track_obj["id"],
                release_date = track_obj["album"]["release_date"],
                release_date_precision = track_obj["album"]["release_date_precision"],
                popularity = track_obj["popularity"]
            )

            # Add it to our result list
            track_metadata.append(current_track_metadata)

    return track_metadata


def get_artist_metadata(track_map: dict[str, list[Track]], credentials: SpotifyAuth) -> list[Track]:
    """
    Returns information about artists like their total followers, popularity and genre based on the passed in `track_list`.
    """
    # Create a list of all the artists
    track_list = list(track_map.values())
    all_artist_ids: list[list[int]] = [[art.id for art in track.artists] for track in track_list]

    # Flatten this list
    flattened_all_artist_ids = [
        x
        for xs in all_artist_ids
        for x in xs
    ]

    # Get unique artist ids
    unique_artist_ids = list(set(flattened_all_artist_ids))

    # NOTE: API restricts us to 50 ids at a time
    CHUNK_SIZE = 50
    # NOTE: So we chunk the incoming artist_ids to chunks of 50
    chunked_artist_ids: list[list[str]] = [unique_artist_ids[idx: idx + CHUNK_SIZE] for idx in range(0, len(unique_artist_ids), CHUNK_SIZE)]

    # Pre-reqs for calling API
    TARGET_URL = "https://api.spotify.com/v1/artists"
    HEADERS = {
        'Authorization': f"Bearer {credentials.access_token}"
    }

    # List to store our parsed vals
    # NOTE: map artist_id to their attributes for easier lookups
    artist_metadata_lookup: dict[str, dict[str, str | list[str] | int]] = {}

    # Call API for each sublist
    for i, chunk in enumerate(chunked_artist_ids):
        print(f"[artist_metadata] Fetching chunk {i} with {len(chunk)} IDs ...")

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
        response_content = response.json()["artists"]
        
        # Convert to TrackMetaData Objects
        for artist_obj in response_content:
            if artist_obj is None:
                continue

            current_artist_data = {
                "genres": artist_obj["genres"],
                "followers": artist_obj["followers"],
                "popularity": artist_obj["popularity"]
            }

            artist_metadata_lookup[artist_obj["id"]] = current_artist_data
    

    # Now, we'll create new Tracks with our artist information
    enriched_tracks: list[Track] = []

    # Iterate over tracks in track_list
    for track in track_list:
        # Populate this in a sub-loop
        enriched_artists: list[Artist] = []

        # Iterate over artists and create an enriched Artist object
        for artist in track.artists:
            current_artist_metadata = artist_metadata_lookup[artist.id]

            enriched_artist_obj = Artist(
                id = artist.id,
                name = artist.name,
                followers = current_artist_metadata["followers"]['total'],
                genres = current_artist_metadata["genres"],
                popularity = current_artist_metadata["popularity"]
            )

            enriched_artists.append(enriched_artist_obj)
        
        # Create new enriched track
        enriched_track = Track(
            id = track.id,
            name = track.name,
            artists = enriched_artists
        )

        # Append to our list above
        enriched_tracks.append(enriched_track)
    
    enriched_track_map = dict(zip(track_map.keys(), enriched_tracks))

    return enriched_track_map



            










