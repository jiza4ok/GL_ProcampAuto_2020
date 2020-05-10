from urllib.parse import urljoin
import allure
import pytest
import requests
from global_scope import BASE_URL
from homework.rest.api_pathes import ITEMS, LOGIN

url_items = urljoin(BASE_URL, ITEMS)
url_login = urljoin(BASE_URL, LOGIN)

# Fixtures

@pytest.fixture()
def get_token(name='test', password='test'):
    """ Get token for JWT """
    response = requests.post(
        url_login,
        json={'username': 'test', 'password': 'test'}
    )
    token = response.json()['access_token']
    print(f'Token: {token}\n')
    response.raise_for_status()
    return token

@pytest.fixture()
def create_new_resource():
    response = requests.post(
        url_items,
        json={'Vitalii': 'Sotnichenko'},
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    item_id = str(response.json()['id']-1)
    yield item_id

@pytest.fixture()
def delete_resource():
    response = requests.delete(
        f'{url_items}/{create_new_resource}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )

@pytest.fixture()
def create_and_delete_resource():
    create_new_resource()
    yield
    delete_resource()


# Tests

@allure.title('Verify authorization with correct credentials')
@pytest.mark.regression
@pytest.mark.smoke
def test_authorization():
    response = requests.post(
        url_login,
        json={'username': 'test', 'password': 'test'}
    )
    access_token = response.json()['access_token']
    assert response.status_code == 200
    assert len(access_token) > 0

@allure.title('Verify authorization with invalid credentials')
@pytest.mark.regression
@pytest.mark.smoke
def test_invalid_authorization():
    response = requests.post(
        url_login,
        json={'username': 'test', 'password': 'pass'}
    )
    assert response.status_code == 401

@allure.title('Create the new resource')
@pytest.mark.regression
@pytest.mark.smoke
def test_create_resource():
    new_item = requests.post(
        url_items,
        json={'Vitalii': 'Sotnichenko'},
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    item_id = str(new_item.json()['id']-1)
    assert new_item.status_code == 201
    assert item_id is not 0

@allure.title('Get the resource')
@pytest.mark.regression
@pytest.mark.smoke
def test_read_resource(create_new_resource):
    response = requests.get(
        f'{url_items}/{create_new_resource}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    resource = response.json()['items']
    assert response.status_code == 200
    assert resource['Vitalii'] == 'Sotnichenko'

@allure.title('delete the resource')
@pytest.mark.smoke
@pytest.mark.regression
def test_delete_resource(create_new_resource):
    response = requests.delete(
        f'{url_items}/{create_new_resource}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    assert response.status_code == 200

@allure.title('Create the resource without token')
@pytest.mark.regression
@pytest.mark.smoke
def test_create_resource_without_token():
    new_item = requests.post(
        url_items,
        json={'Vitalii': 'Sotnichenko'},
        headers={'Authorization': f'Bearer'}
    )
    assert new_item.status_code == 422
    assert new_item.json()['msg'] == "Bad Authorization header. Expected value 'Bearer <JWT>'"