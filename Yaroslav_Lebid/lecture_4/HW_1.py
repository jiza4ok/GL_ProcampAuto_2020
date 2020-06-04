import requests 
from requests.exceptions import HTTPError 

username = 'test'
password = 'bye'

for url in ['http://localhost:5002/basic_auth', 'http://localhost:5002/', 'http://localhost:5002/fail500']: 
    try: 
        print(f"\nSending GET request to {url}") 
        if url.find("basic_auth"):
            response = requests.get(url, auth=(username, password))
        else:
            response = requests.get(url) 
        response.raise_for_status() 

    except HTTPError as http_err:  
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')