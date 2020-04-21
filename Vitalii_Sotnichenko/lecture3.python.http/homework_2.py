import requests
from requests.auth import HTTPBasicAuth

response = requests.get('http://localhost:5002/')
print(response.status_code)
response = requests.get('http://localhost:5002/fail500')
print(response.status_code)
response = requests.get('http://localhost:5002/users')
print(response.status_code)

response = requests.get('http://localhost:5002/')
print(response.json())

response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'GL_ProcampAuto_2020'},
)

#Анализ некоторых атрибутов местонахождения запроса
json_response = response.json()
repository = json_response['items'][0]
print(f'Repository name: {repository["name"]}')
print(f'Repository description: {repository["description"]}')


response = requests.post(
    'http://localhost:5002/',
    json={'vsot':'value'}
)

json_response = response.json()
print(f'Response: {json_response}')

response = requests.get(
    'http://localhost:5002/basic_auth',
    auth=HTTPBasicAuth('sergii', 'hello')
)
print(response.text)

response = requests.post(
    'http://localhost:5002/login',
    json={'username': 'test', 'password': 'test'}
    )
token = response.json()['access_token']
print(f'Token: {token}\n')

print("Send not authoraized request")
response = requests.get('http://localhost:5002/protected')
print(response.text)

print("Send authoraized request")
response=requests.get(
    'http://localhost:5002/protected',
    headers={'Authorization': f'Bearer {token}'})
print(response.text)

# Create new item
item = requests.post(
    'http://localhost:5002/items',
    json = {'Vitalii': 'Sotnichenko'},
    headers = {'Authorization': f"Bearer {token}"}
)

item_id = str(item.json()['id'])
print(item_id)

# Delete item
response = requests.delete(
    'http://localhost:5002/items/' + item_id,
    headers = {'Authorization': f"Bearer {token}"}
)
print(response.status_code)