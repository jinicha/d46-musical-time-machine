import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

import config

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"

BASE_URL = "https://www.billboard.com/charts/hot-100/"

date = input('Which year do you want to travel to? (in format YYYY-MM-DD): ')
response = requests.get(f'{BASE_URL}{date}/')
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select("ul li h3")[:100]
song_title = [song.get_text().strip('\n') for song in songs]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True,
        cache_path="token.txt"
    ),
)
user_id = sp.me()["id"]
year = date.split("-")[0]
client_list = []
for title in song_title:
    result = sp.search(q=f'track{title} year:{year}')
    try:
        uri = result["tracks"]["items"][0]["uri"]
        client_list.append(uri)
        print(f'Added {title}!')
    except IndexError:
        print(f'{title} not found')

create_list_response = sp.user_playlist_create(
    user=user_id,
    name=f'{date} Billboard 100',
    public=False,
    description="test"
)
playlist_id = create_list_response["id"]
pprint(create_list_response)
