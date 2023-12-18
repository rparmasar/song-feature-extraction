from os import environ
from dotenv import load_dotenv

from src.auth import get_spotify_token
from src.pipeline import get_track_attributes
from src.data_fetching.search_strategies import PLAYLIST_ID_MAP



def main():
    # Loading environment variables
    load_dotenv(override=True)

    # get auth token
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")

    current_auth = get_spotify_token(CLIENT_ID, CLIENT_SECRET)

    # get dataframe
    attribute_df = get_track_attributes(
        source='playlist',
        id_map=PLAYLIST_ID_MAP,
        credentials=current_auth
    )

    print(attribute_df)

    # write to csv
    attribute_df.to_csv('track-attributes.csv', index=False)



if __name__ == "__main__":
    main()