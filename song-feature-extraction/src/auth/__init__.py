import requests
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SpotifyAuth:
    access_token: str
    expires_in: str
    time_til_refresh: datetime = datetime.now()


def get_spotify_token(client_id: str, client_secret: str) -> SpotifyAuth:
    """
    Queries the Spotify API auth endpoint to return a token for making authenticated requests.
    """

    URL = "https://accounts.spotify.com/api/token"

    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    DATA = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(URL, headers=HEADERS, data=DATA)
    json_response = response.json()
    print(json_response)
    
    response_content = SpotifyAuth(
        **{key:val for (key, val) in json_response.items() if key in SpotifyAuth.__dataclass_fields__}
    )

    return response_content

