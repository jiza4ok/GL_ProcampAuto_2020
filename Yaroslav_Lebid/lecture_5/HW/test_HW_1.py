import pytest
import requests

BASE_URL = "http://localhost:5002/"
BASE_URL_ITEMS = "http://localhost:5002/items"

# fixture to get token
@pytest.fixture()
def token():
    response = requests.post(
        BASE_URL + 'login',
        json = {'username': 'test', 'password': 'test'}
    )
    token = response.json()['access_token']
    return token

# fixture to create item
@pytest.fixture()
def new_item(token):
    response = requests.post(
        BASE_URL_ITEMS,
        json = {'item': 'newItem'},
        headers = {'Authorization': f"Bearer {token}"}
    )
    new_item = int(response.json()['id']-1)

    yield new_item

    requests.delete(
    BASE_URL_ITEMS + str(new_item),
    headers = {'Authorization': f"Bearer {token}"}
    )

# fixture to delete item
@pytest.fixture()
def delete_item(token, new_item):
    requests.delete(
        BASE_URL_ITEMS + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )

############## Tests ################

# Check if server is Up and running
#0
@pytest.mark.build_acceptance
@pytest.mark.smoke
@pytest.mark.regression
def test_0_server_up():
    response = requests.get(
        BASE_URL_ITEMS
    )
    assert response.status_code == 401

# Authorization/Login Tests
#1
@pytest.mark.smoke
@pytest.mark.regression
def test_1_authoryze():
    response = requests.post(
        BASE_URL + 'login',
        json = {'username': 'test', 'password': 'test'}
    )
    status_code = response.status_code
    token = response.json()['access_token']

    assert status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert len(token) > 0

#2
@pytest.mark.smoke
@pytest.mark.regression
def test_2_login_with_token(token):
    response = requests.get(
    BASE_URL + 'protected',
    headers={'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code

    assert status_code == 200

# Create new item
#3
@pytest.mark.smoke
@pytest.mark.regression
def test_3_create_item(token):
    response = requests.post(
        BASE_URL_ITEMS,
        json = {'item': 'newItem'},
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code
    new_item_id = int(response.json()['id']-1)

    assert status_code == 201
    assert response.headers['Content-Type'] == "application/json"
    assert new_item_id > 0

# Create new item one by one
#4
@pytest.mark.smoke
@pytest.mark.regression
def test_4_create_items_one_by_one(token):
    response1 = requests.post(
        BASE_URL_ITEMS,
        json = {'item': 'newItem'},
        headers = {'Authorization': f"Bearer {token}"}
    )
    new_item_id_1 = int(response1.json()['id']-1)

    response2 = requests.post(
        BASE_URL_ITEMS,
        json = {'item': 'newItem'},
        headers = {'Authorization': f"Bearer {token}"}
    )
    new_item_id_2 = int(response2.json()['id']-1)

    assert new_item_id_2 == new_item_id_1 + 1

# Check if new item is available
#5
@pytest.mark.smoke
@pytest.mark.regression
def test_5_item_created(token, new_item):
    response = requests.get(
        BASE_URL_ITEMS + "/" + str(new_item), 
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code

    assert status_code == 200

#6 delete just created item
@pytest.mark.smoke
@pytest.mark.regression
def test_6_delete_item(new_item, token):
    response = requests.delete(
        BASE_URL_ITEMS + "/" + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code

    assert status_code == 200

#7 delete and check if still avilable
@pytest.mark.smoke
@pytest.mark.regression
def test_7_if_available_after_deletion(new_item, token):
    requests.delete(
        BASE_URL_ITEMS + "/" + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )
   
    response2 = requests.get(
        BASE_URL_ITEMS + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response2.status_code

    assert status_code == 404

# Negative scenarios
#1 
### try to authoryze with wrong user 
@pytest.mark.regression
def test_negative_1_cannot_authoryze():
    response = requests.post(
        BASE_URL + 'login',
        json = {'username': 'testx', 'password': 'test'}
    )
    status_code = response.status_code

    assert status_code == 401

#2
### try to create item w/o authorization
@pytest.mark.regression
def test_negative_2_create_item_wo_auth():
    response = requests.post(
        BASE_URL_ITEMS,
        json = {'item': 'newItem'}
    )
    status_code = response.status_code

    assert status_code == 401

#3
### try to get item w/o authorization
@pytest.mark.regression
def test_negative_3_get_item_wo_auth(new_item):
    response = requests.get(
        BASE_URL_ITEMS + "/" + str(new_item)
    )
    status_code = response.status_code

    assert status_code == 401

#4
### try to get unexistent item
@pytest.mark.regression
def test_negative_4_get_unexistent_item(new_item, token):
    response = requests.get(
        BASE_URL_ITEMS + "/" + str(new_item+100), 
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code

    assert status_code == 400

#5 delete already deleted item
@pytest.mark.regression
def test_negative_5_delete_deleted_item(new_item, token):
    requests.delete(
        BASE_URL_ITEMS + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )
    response = requests.delete(
        BASE_URL_ITEMS + str(new_item),
        headers = {'Authorization': f"Bearer {token}"}
    )
    status_code = response.status_code
    
    assert status_code == 404