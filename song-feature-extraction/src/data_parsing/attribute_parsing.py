# handles creating a dataframe from the attributes response returned
import pandas as pd
from ..data_types import TrackAttributes, Track, TrackAttributeColumns, TrackAttributeDataFrame, TrackMetaData

def create_track_attribute_dataframe(track_attributes: list[TrackAttributes], track_list: list[Track], track_metadata: list[TrackMetaData]) -> TrackAttributeDataFrame:
    """
    Creates and returns a `TrackAttributeDataFrame` by converting the `track_attributes` and `track_list` to a dataframe and then joining on `track_id`.
    """
    # Create initial attribute dataframe
    track_attr_df: TrackAttributeDataFrame = pd.DataFrame([track_attr.to_dict() for track_attr in track_attributes])

    # Convert Tracks to dataframe
    track_info_df = pd.DataFrame([track.to_dict() for track in track_list])

    # Convert Track metadata to dataframe
    track_metadata_df = pd.DataFrame([track_met.to_dict() for track_met in track_metadata])

    # Join metadata to track info df
    track_info_df = track_info_df.merge(
        right=track_metadata_df,
        on=TrackAttributeColumns.ID.value
    )

    # Join on `id` col
    result_df = pd.merge(
        left=track_attr_df,
        right=track_info_df,
        how='left',
        on=TrackAttributeColumns.ID.value
    )

    return result_df