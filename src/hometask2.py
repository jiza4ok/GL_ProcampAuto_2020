import requests

# login and get access token
HOST = 'http://localhost:5002'

auth_info = requests.post(
    '{}/login'.format(HOST),
    json={'username': 'test', 'password': 'test'}
)
token = auth_info.json()['access_token']

# post new item
new_item = requests.post(
    '{}/items'.format(HOST),
    headers={'Authorization': f"Bearer {token}"},
    json={'Kateryna': 'Lysenko'}
)
id_of_new_item = new_item.json()['id']
print(f"added new item", new_item.text)
print("id of new item is: ", id_of_new_item)

# get items
all_items = requests.get(
    '{}/items'.format(HOST),
    headers={'Authorization': f"Bearer {token}"}
)
print(f"items in the list:", all_items.text)

# delete created item
delete_item_response = requests.delete(
    '{host}/items/{id_of_new_item}'.format(
        host=HOST,
        id_of_new_item=id_of_new_item
    ),
    headers={'Authorization': f"Bearer {token}"}
)
print(delete_item_response.text)
