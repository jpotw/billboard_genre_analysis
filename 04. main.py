import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import os
import requests
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(429, 500, 502, 503, 504), session=None):
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

endpoint = "https://api.spotify.com/v1/artists/{id}"
access_token = ""

try:
    billboard_data = pd.read_csv('billboard_data.csv')
    print("billboard_data.csv 파일 읽기 완료")
except FileNotFoundError:
    print("Error: 'billboard_data.csv' file not found.")
    exit(1)

try:
    client_id = ''
    client_secret = ''
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_session=requests_retry_session())
    print("Spotify 인증 완료")
except spotipy.oauth2.SpotifyOauthError as e:
    print(f"Error: {e}")
    exit(1)

batch_size = 100  # Adjust the batch size as needed
total_batches = len(billboard_data) // batch_size + 1

artist_genres = {}  # Dictionary to store artist genres

for batch_number in range(total_batches):
    start_index = batch_number * batch_size
    end_index = min((batch_number + 1) * batch_size, len(billboard_data))
    subset = billboard_data[start_index:end_index]

    genres_data = []
    for i, row in subset.iterrows():
        date = row['date']
        rank = int(row['rank'])
        song_title = row['song_title']
        artist = row['artist']
        
        if artist in artist_genres:
            genres = artist_genres[artist]
            genres_data.append({'date': date, 'rank': rank, 'song_title': song_title, 'artist': artist, 'genres': genres})
            print(f"{batch_number+1}번째 set의 {rank}. 가수: {artist} 장르: {genres}")
        else:
            query = f'track:{song_title} artist:{artist}'
            
            try:
                result = sp.search(q=query, type='track', limit=1)
                artist_id = result['tracks']['items'][0]['artists'][0]['id'] if result['tracks']['items'] else None
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }

                response = requests.get(endpoint.format(id=artist_id), headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    genres = data["genres"]
                    artist_genres[artist] = genres
                    genres_data.append({'date':date, 'rank': rank, 'song_title': song_title, 'artist': artist, 'genres': genres})
                    print(f"{batch_number+1}번째 set의 {rank}. 가수: {artist} 장르: {genres}")
                else:
                    print(f"{date}의 {artist}의 {song_title} 요청이 실패했습니다. 상태 코드:", response.status_code)
                    genres_data.append({'song_title': song_title, 'artist': artist, 'genres': "Need Manual Check"})
            except spotipy.SpotifyException as e:
                if e.http_status == 429:
                    print("API 요청이 차단되었습니다. 잠시 후 다시 시도해주세요.")
                else:
                    print(f"API 요청 중 오류 발생: {e}")
                    genres_data.append({'song_title': song_title, 'artist': artist, 'genres': []})
            except HTTPError as e:
                if e.response.status_code == 429:
                    retry_after = int(e.response.headers.get('Retry-After', 1))
                    print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    print(f"Error retrieving data for {song_title} by {artist}: {e}")
                    genres_data.append({'song_title': song_title, 'artist': artist, 'genres': []})
            except Exception as e:
                print(f"Error processing {song_title} by {artist}: {e}")
                genres_data.append({'song_title': song_title, 'artist': artist, 'genres': []})
    
    genre_df = pd.DataFrame(genres_data)
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'genres_data_batch_{batch_number + 1}.csv')
    genre_df.to_csv(output_path, index=False)
    print(f"Genres data for batch {batch_number + 1} saved to: {output_path}")

print("모든 batch 작업 완료")
print("장르 수집 완료")