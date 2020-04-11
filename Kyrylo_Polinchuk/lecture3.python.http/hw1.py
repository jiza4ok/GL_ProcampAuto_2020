import requests
url0='http://localhost:5002/'
response1=requests.post(url0+'login', json={'username': 'test', 'password':'test'})
print(response1.json())
response2=requests.post(url0, data="item")
response3=requests.get(url0, params="item").json()
response4=requests.delete(url0)
print(response2)
print(response3)
print(response4)

from requests.exceptions import HTTPError
for url in ['http://localhost:5002/','http://localhost:5002/fail500', 'http://localhost:5002/users']:
    try:
        print(f'\nSending Get request to {url}')
        response5=requests.get(url)
        response5.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured:{err}')
    else:
        print("Success")

print(response5)
print(response5.raise_for_status())