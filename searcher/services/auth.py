import requests
import json
from datetime import datetime, timedelta
from . import storage


def create_initial_tokens(client_data):
    path = '/oauth2/access_token'
    domain = client_data["base_domain"]
    subdomain = client_data["subdomain"]
    URL = f'https://{subdomain}.{domain}{path}'
    sent_data = {
        'client_id': client_data["client_id"],
        'client_secret': client_data["client_secret"],
        'grant_type': 'authorization_code',
        'code': client_data["authorization_code"],
        'redirect_uri': client_data["redirect_uri"],
    }
    headers = {'Content-type': 'application/json', 'User-Agent': 'amoCRM-oAuth-client/1.0'}
    response = requests.post(URL, data=json.dumps(sent_data), headers=headers)
    auth_data = response.json()
    auth_data["tokens_created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    storage.save_tokens(auth_data, subdomain)
    return auth_data


def refresh_tokens(refresh_token):
    client_data = storage.load_client_data()
    subdomain = client_data["subdomain"]
    base_domain = client_data["base_domain"]
    path = '/oauth2/access_token'
    URL = f'https://{subdomain}.{base_domain}{path}'

    sent_data = {
        'client_id': client_data["client_id"],
        'client_secret': client_data["client_secret"],
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': client_data["redirect_uri"],
    }

    headers = {'Content-type': 'application/json', 'User-Agent': 'amoCRM-oAuth-client/1.0'}
    response = requests.post(URL, data=json.dumps(sent_data), headers=headers)
    auth_data = response.json()
    auth_data["tokens_created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    storage.save_tokens(auth_data, subdomain)

    return auth_data


def is_access_token_expired(created_date, expires_in):
    expires_on = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S") + timedelta(0, expires_in)
    print(expires_on)
    return datetime.now() >= expires_on
