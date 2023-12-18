from dataclasses import dataclass, asdict
from pandas import DataFrame
from enum import Enum

@dataclass
class Artist:
    id: str
    name: str


@dataclass(kw_only=True)
class Track:
    id: str
    name: str
    artists: list[Artist]

    def to_dict(self) -> dict[str, str]:
        """
        Returns a flattened version of the `Track` that is suitable for creating a dataframe.
        """
        res = {
            'track_id': self.id,
            'track_name': self.name,
            'track_artists_id': ",".join([art.id for art in self.artists]),
            'track_artists_name': ",".join([art.name for art in self.artists])
        }

        return res
    

@dataclass
class TrackAttributes:
    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int

    def to_dict(self) -> dict[str, str | float | int]:
        res_dict = asdict(self)
        # Easier for joining later on
        res_dict[TrackAttributeColumns.ID.value] = res_dict['id']
        del res_dict['id']
        return res_dict

    

class TrackAttributeDataFrame(DataFrame):
    """
    A `pandas::DataFrame` mapping track IDs to their track attributes, names and artists
    """


class TrackAttributeColumns(Enum):
    """
    For further desciptions, see [Spotify API | get-several-audio-features](https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features)
    """
    ID: str = 'track_id'
    NAME: str = 'track_name'
    ARTISTS_IDS: str = 'artist_ids'
    ARTISTS_NAMES: str = 'artist_names'
    DANCEABILITY: float = 'danceability'
    ENERGY: float = 'energy'
    KEY: int = 'key'
    LOUDNESS: float = 'loudness'
    MODE: int = 'mode'
    SPEECHINESS: float = 'speechiness'
    ACOUSTICNESS: float = 'acousticness'
    INSTRUMENTALNESS: float = 'instrumentalness'
    LIVENESS: float = 'liveness'
    VALENCE: float = 'valence'
    TEMPO: float = 'temp'
    DURATION_MS: int = 'duration_ms'
    TIME_SIGNATURE: int = 'time_signature'


class Source(Enum):
    PLAYLIST = 'playlist'
    ARTIST = 'artist'