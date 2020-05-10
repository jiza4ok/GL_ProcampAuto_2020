import requests
from global_scope import BASE_URL
from homework.rest.api_pathes import FAIL, USERS
from requests.exceptions import HTTPError

for url in [BASE_URL, BASE_URL + FAIL, BASE_URL + USERS]:
    try:
        print(f'\nSend Get request to {url}')
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other errors occured:{err}')
    else:
        print("Success")
