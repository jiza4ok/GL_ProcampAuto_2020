import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin


BASE_URL = 'http://0.0.0.0:5002'
ENDPOINTS = ['/', '/fail500', '/basic_auth']

for endpoint in ENDPOINTS:
    url = urljoin(BASE_URL, endpoint)
    try:
        print(f'\nSending GET request to {url}')
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error occurred: {http_err}')
    except Exception as err:
        print(f'Other Error occurred: {err}')
    else:
        print("SUCCESS")
