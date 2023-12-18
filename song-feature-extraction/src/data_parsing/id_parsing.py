# handles constructing an efficient list for which we'll fetch song attributes for
from ..data_types import Track, Artist

from pprint import pprint

def create_consolidated_tracks(*track_lists: list[Track]) -> dict[str, Track]:
    """
    Given several lists of `Track`s, return one list with no duplicate `Track` objects based on their `id`
    """
    # Create dict for storing Tracks
    unique_tracks = {}

    # Iterate over lists and try to add to our resulting dict
    for track_list in track_lists:
        delta_tracks = {track.id: track for track in track_list if track is not None and track.id not in unique_tracks}

        unique_tracks.update(delta_tracks)
    
    total_tracks_length = sum(len(tl) for tl in track_lists)
    final_length = len(unique_tracks.keys())
    print(f"Found {final_length} unique Tracks from an initial {total_tracks_length} Tracks!")
    
    return(unique_tracks)







