from os import environ
from dotenv import load_dotenv

from src.auth import get_spotify_token
from src.data_fetching import get_artist_tracks, ARTIST_ID_MAP, get_playlist_tracks, get_tracks_attributes

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
    # TEST_PLAYLIST_ID="6Jq0QdwB0vk7VPcIqpo4pr"
    # print(test)
    # test = get_playlist_tracks(
    #     # playlist_id="0BBqSucRp5ePvhNUSCPAgx",
    #     playlist_id="6Jq0QdwB0vk7VPcIqpo4pr",
    #     credentials=current_auth
    # )
    test = get_tracks_attributes(
        tracks_ids=['5wPcFRwPMK1aVhboTtJK5f', '0MCA6RAlibvowsEaZy9p8y', '3KowpMVfbYubAEk68w8qT1'],
        credentials=current_auth
    )

    with open("track-features.json", "w") as jf:
        json.dump(test, jf, indent=2)







if __name__ == "__main__":
    main()