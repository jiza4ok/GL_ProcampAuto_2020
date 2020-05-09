from urllib.parse import urljoin

import requests
from global_scope import base_url
from homework.rest import api_pathes
from homework.rest.api_pathes import items, login
url_items = urljoin(base_url, api_pathes.items)


def authorization_and_get_token(name='test', password='test'):
    """ Get token for JWT """
    response = requests.post(
        base_url + login,
        json={'username': 'test', 'password': 'test'}
    )
    token = response.json()['access_token']
    print(f'Token: {token}\n')
    response.raise_for_status()
    return token

def create_resource():
    """ Create resource
    :return item_id of created resource """
    new_item = requests.post(
        url_items,
        json={'Vitalii': 'Sotnichenko'},
        headers={'Authorization': f'Bearer {authorization_and_get_token()}'}
    )
    item_id = str(new_item.json()['id']-1)
    print(item_id)
    return item_id

def read_resource(item_id):
    """ Get the created resource"""
    response = requests.get(
        f'{url_items}/{item_id}',
        headers={'Authorization': f'Bearer {authorization_and_get_token()}'}
    )
    print(f"Get resource with id '{create_resource()}'")
    resource = response.json()['items']
    print(resource)

def delete_resource(item_id):
    """ Delete the resource
    :param item_id:
    :return: none
    """
    response = requests.delete(
        f'{base_url}{items}/{item_id}',
        headers={'Authorization': f'Bearer {authorization_and_get_token()}'}
    )
    print(response.status_code)

if __name__ == '__main__':
    authorization_and_get_token('test', 'test')
    item_id = create_resource()
    read_resource(item_id)
    delete_resource(item_id)