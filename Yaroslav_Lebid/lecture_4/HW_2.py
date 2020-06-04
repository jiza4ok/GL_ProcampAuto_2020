import requests 
import urllib
from urllib.parse import urljoin

# basic server URL
BASE_URL = 'http://localhost:5002/'

username = 'test'
password = 'test'
login_json = {'username': username, 'password': password}

# 1 Get token and check Authorization
response = requests.post(
    urljoin(BASE_URL, 'login'), 
    json = login_json)

token = response.json()['access_token']
print(f"\n1.1 Token received:\n{token}")
print(f"Raise_for_status: {response.raise_for_status()}\n")

# for futher usage in requests as 'headers'
authorization_header = {'Authorization': f"Bearer {token}"}

response1 = requests.get(
    urljoin(BASE_URL, 'protected'),
    headers = authorization_header
)
print("1.2 Can LOGIN with token")
print("Expected status code: 200")
print(f"Received status code: {response1.status_code}")
print(f"Raise_for_status: {response1.raise_for_status()}\n")

# 2 post new item and get item ID
response2 = requests.post(
    urljoin(BASE_URL, 'items'),
    json = {'item': 'newItem'},
    headers = authorization_header
)
print("2.1 CREATE Item by POST")
print("Expected status code: 201")
print(f"Received status code: {response2.status_code}")
print(f"Raise_for_status: {response2.raise_for_status()}\n")

print(f"2.2 CREATED Item by POST, ID for new item received: {response2.json()}\n")

# Save responce ID for new item to new_item_id
# -1 => because of bug in symple-app.py
new_item_id = response2.json()['id']-1

# created item partial URL (looks like: "items/<new_item_id>")
item_partial_URL = 'items/' + str(new_item_id)

# full URL to just created item (looks like: "http://localhost:5002/items/<new_item_id>")
new_item_URL = urljoin(BASE_URL, item_partial_URL)

# 3. Check if new item available
response3 = requests.get(
    new_item_URL,
    headers = authorization_header
)
print("3. Check if item is created (send GET)")
print("Expected status code: 200")
print(f"Received status code: {response3.status_code}")
print(f"Raise_for_status: {response3.raise_for_status()}\n")

#4 delete just created item
response4 = requests.delete(
    new_item_URL,
    headers = authorization_header
)
print("4. DELETE item")
print("Expected status code: 200")
print(f"Received status code: {response4.status_code}")
print(f"Raise_for_status: {response4.raise_for_status()}\n")

#5 Check if item still available 
response5 = requests.get(
    new_item_URL,
    headers = authorization_header
)
print("5. Check if item still available(send GET for the deleted item)")
print("Expected status code: 404 (Not Found), but actually 400 will be returned because of bug in test-app.py")
print(f"Received status code: {response5.status_code}\n")
print(f"Raise_for_status: {response5.raise_for_status()}\n")