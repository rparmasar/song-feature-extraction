# High-level functions to fetch data
from .data_fetching import get_playlist_tracks, get_tracks_attributes, get_tracks_metadata, get_artist_metadata
from .data_parsing import create_consolidated_tracks, create_track_attribute_dataframe

from .data_types import Source, TrackAttributeDataFrame, Track, TrackAttributes, TrackMetaData, TrackAttributeColumns
from .auth import SpotifyAuth

from time import perf_counter
from datetime import datetime


def get_track_attributes_from_artist(id_map: dict[str, str], credentials: SpotifyAuth) -> TrackAttributeDataFrame:
    """
    # TODO: Implement
    """
    raise NotImplementedError()


def get_track_attributes_from_playlist(id_map: dict[str, str], credentials: SpotifyAuth) -> TrackAttributeDataFrame:
    """
    Returns a `TrackAttributeDataFrame` from the playlists provided.
    """
    # Get lists of Tracks
    playlist_tracks: dict[str, list[Track]] = {id: None for id in id_map.values()}

    for playlist_name, playlist_id in id_map.items():
        start = perf_counter()

        print(f"Fetching IDs for {playlist_name=} ...")

        # Compute track IDs and store in the above dict
        playlist_tracks[playlist_id] = get_playlist_tracks(
            playlist_id=playlist_id,
            credentials=credentials
        )
        elapsed = perf_counter() - start
        print(f"Finished processing {len(playlist_tracks[playlist_id])} tracks from {playlist_name} in {elapsed:.2f} seconds!")
    
    # Consolidate IDs
    consolidated_tracks: dict[str, Track] = create_consolidated_tracks(
        *playlist_tracks.values()
    )

    # Fetch artist metadata
    enriched_tracks: dict[str, Track] = get_artist_metadata(
        track_map=consolidated_tracks,
        credentials=credentials
    )

    consolidated_ids = list(enriched_tracks.keys())

    # Fetch track metadata
    track_metadata: list[TrackMetaData] = get_tracks_metadata(
        tracks_ids=consolidated_ids,
        credentials=credentials
    )

    # Fetch attribute information
    track_attributes: list[TrackAttributes] = get_tracks_attributes(
        tracks_ids=consolidated_ids,
        credentials=credentials
    )

    # Create result dataframe
    result_df = create_track_attribute_dataframe(
        track_attributes=track_attributes,
        track_list=list(enriched_tracks.values()),
        track_metadata=track_metadata
    )

    # Add generated column for auditing
    result_df[TrackAttributeColumns.GENERATED_TIMESTAMP.value] = datetime.now().strftime("%Y-%m-%d")

    return result_df

    

def create_track_attribute_df(source: Source, id_map: dict[str, str], credentials: SpotifyAuth) -> TrackAttributeDataFrame:
    """
    """
    if source == Source.PLAYLIST.value:
        res_df = get_track_attributes_from_playlist(
            id_map=id_map,
            credentials=credentials
        )
        return res_df
    
    elif source == Source.ARTIST.value:
        get_track_attributes_from_artist()
    
    else:
        raise NotImplementedError()
    