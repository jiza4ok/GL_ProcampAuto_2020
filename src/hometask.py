import requests
from requests.auth import HTTPBasicAuth

response = requests.post('http://localhost:5002/login',
                         json={'username': 'test', 'password': 'test'})
token = response.json()['access_token']

response2 = requests.post('http://localhost:5002/items',
                          headers={'Authorization': f"Bearer {token}"},
                          json={'Kateryna': 'Lysenko'}
                          )
id_of_new_item = response2.json()['id']
print(f"added new item", response2.text)
print("id of new item is: ", id_of_new_item)

response1 = requests.get('http://localhost:5002/items',
                         headers={'Authorization': f"Bearer {token}"}
                         )
print(f"items in the list:", response1.text)

response3 = requests.delete('http://localhost:5002/items/{id_of_new_item}'.format(id_of_new_item=0),
                            headers={'Authorization': f"Bearer {token}"}
                            )
print(response3.text)

for item in response1.json()['items']:
    response4 = requests.delete('http://localhost:5002/items/{id_of_new_item}'.format(id_of_new_item=0),
                                headers={'Authorization': f"Bearer {token}"}
                                )
    print(response4.status_code)
