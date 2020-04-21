import requests

from requests.exceptions import HTTPError
for url in ['http://localhost:5002/','http://localhost:5002/fail500', 'http://localhost:5002/users']:
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
