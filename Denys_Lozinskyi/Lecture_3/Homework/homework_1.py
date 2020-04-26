import requests
from requests.exceptions import HTTPError

URL = 'http://0.0.0.0:5002/'
endpoints = ['', 'fail500', 'basic_auth']

for endpoint in endpoints:
    url = URL + endpoint
    try:
        print('\nSending GET request to {}'.format(url))
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP Error occurred: {}'.format(http_err))
    except Exception as err:
        print('Other Error occurred: {}'.format(err))
    else:
        print("SUCCESS")
