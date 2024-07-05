import requests
import base64

client_id = 
client_secret = 

auth_url = 'https://accounts.spotify.com/api/token'
auth_headers = {
    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
}
auth_data = {
    'grant_type': 'client_credentials'
}

response = requests.post(auth_url, headers=auth_headers, data=auth_data)

if response.status_code == 200:
    token = response.json()['access_token']
    print(token)
else:
    print('Error:', response.status_code)