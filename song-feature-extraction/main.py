from os import environ
from dotenv import load_dotenv

from src.auth import get_spotify_token
from src.data_fetching import get_artist_tracks, ARTIST_ID_MAP, get_playlist_tracks

import json


def main():
    # Loading environment variables
    load_dotenv(override=True)

    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")

    current_auth = get_spotify_token(CLIENT_ID, CLIENT_SECRET)

    # test = get_artist_tracks(
    #     artist_id=ARTIST_ID_MAP["Prince Swanny"],
    #     credentials=current_auth
    # )

    # print(test)
    test = get_playlist_tracks(
        # playlist_id="0BBqSucRp5ePvhNUSCPAgx",
        playlist_id="6Jq0QdwB0vk7VPcIqpo4pr",
        credentials=current_auth
    )

    with open("playlist-output-paginated.json", "w") as jf:
        json.dump(test, jf, indent=2)







if __name__ == "__main__":
    main()