import requests 
from requests.exceptions import HTTPError 
 
for url in ['http://localhost:5002/', 'http://localhost:5002/fail500', 'http://localhost:5002/basic_auth']: 
    try: 
        print(f"\nSending GET request to {url}") 
        response = requests.get(url) 

        response.raise_for_status() 
        json_responce = response.json()

    except HTTPError as http_err:  
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')