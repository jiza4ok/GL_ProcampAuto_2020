import requests
from global_scope import base_url
from homework.rest.api_pathes import fail, users
from requests.exceptions import HTTPError

for url in [base_url, base_url + fail, base_url + users]:
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
