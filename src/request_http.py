import requests
from requests.auth import HTTPBasicAuth

response = requests.get('http://localhost:5002')
print(requests.get('http://localhost:5002'))

print(response.__dict__)
print(response.status_code)
print(response.json())

response2 = requests.get('http://localhost:5002/fail500')
print(response2.status_code)
response3 = requests.get('http://localhost:5002/users')
print(response2.status_code)

response4 =requests.post(
    'http://localhost:5002/fail500',
    json={'serbut':'value'})
json_response = response4.json()
print('Response:{json_response}')

response5 = requests.get('http://localhost:5002/basic_auth',
                         auth=HTTPBasicAuth('sergii','hello'))
print(response5.text)

response6 = requests.post('http://localhost:5002/login',
                         json={'username':'test', 'password':'test'})
token = response6.json()['access_token']
print(response6.json())
print(f"token:{token}\n")



#GitHub
response44 = requests.get('https://api.github.com/search/repositories', params={'q': 'GL_ProcampAuto_2020'})
json_response = response44.json()
repository = json_response['items'][0]
