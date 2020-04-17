import requests

# 1 Get token and check Authorization
response = requests.post(
    'http://localhost:5002/login',
    json = {'username': 'test', 'password': 'test'}
)
token = response.json()['access_token']
print(f"\n1.1 Token received:\n{token}\n")

response1 = requests.get(
    'http://localhost:5002/protected',
    headers={'Authorization': f"Bearer {token}"}
    )
print(f"1.2 Can Login with token, status code: {response1.status_code}\n")

# 2 post new item and get item ID
response2 = requests.post(
    'http://localhost:5002/items',
    json = {'item': 'newItem'},
    headers = {'Authorization': f"Bearer {token}"}
)

print(f"2.1 Create Item by POST, response status code: {response2.status_code}\n")
print(f"2.2 Create Item by POST, ID for new item: {response2.json()}\n")
#responce ID for new item to newItemID
newItemId = str(response2.json()['id']-1)

# 3. Check if new item available
response3 = requests.get(
    'http://localhost:5002/items/' + newItemId, 
     headers = {'Authorization': f"Bearer {token}"}
)
print(f'3. Check if item is created (send GET), response status code: {response3.status_code}\n')

#4 delete just created item
response4 = requests.delete(
    'http://localhost:5002/items/'+ newItemId,
    headers = {'Authorization': f"Bearer {token}"}
)
print(f'4. DELETE item, response status code: {response4.status_code} \n')

#5 Check if item still available 
response5 = requests.get(
    'http://localhost:5002/items/' + newItemId, 
     headers = {'Authorization': f"Bearer {token}"}
)
print(f'5. Check if item still available(send GET for the item), status code: {response5.status_code}\n')
