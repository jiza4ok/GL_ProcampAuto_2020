#! /usr/bin/python3.7
import requests
from requests.exceptions import HTTPError
from urllib.parse import urljoin
import Denys_Lozinskyi.Lecture_3.homework.api as api


url_login = urljoin(api.base_url, api.login_endpoint)
url_protected = urljoin(api.base_url, api.protected_endpoint)
url_items = urljoin(api.base_url, api.items_endpoint)

access_token = ''


def authorize(user_name: str, password: str):
    """ Does authorization at the server by JWT """
    try:
        response = requests.post(
            url_login, json={'username': user_name, 'password': password}
        )
        print(f'\nLOGGING IN as "{user_name}"')
        global access_token
        access_token = response.json()['access_token']
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error at submitting credentials: {http_err}')
    except Exception as err:
        print(f'Error at submitting credentials: {err}')

    try:
        response = requests.get(
            url_protected, headers={'Authorization': f'Bearer {access_token}'}
        )
        print(f'AUTHORIZATION...')
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error in authorization with token: {http_err}')
    except Exception as err:
        print(f'Error in authorization with token: {err}')
    else:
        print(f'Authorization complete. Logged in as "{user_name}"')


def create_resource(item: dict) -> str:
    """ Creates a resource with a 'name' provided
        :param item: name of the resource to be created
        :return :int: the ID of the item created
    """
    try:
        response = requests.post(
            url_items, json=item, headers={'Authorization': f'Bearer {access_token}'}
        )
        print(f'\nCREATING THE RESOURCE "{item}"')
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error in the resource creation: {http_err}')
    except Exception as err:
        print(f'Error in the resource creation: {err}')
    else:
        res_id = str(response.json()['id'] - 1)
        print(f'Resource "{item}" is created with ID: "{res_id}"')
        return res_id


def read_resource(res_id: str):
    """ Reads the resource content by the resource ID
        :param res_id: ID of the resource
    """
    try:
        response = requests.get(
            f'{url_items}/{res_id}', headers={'Authorization': f'Bearer {access_token}'}
        )
        print(f'\nREADING THE RESOURCE with ID "{res_id}"')
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error at the resource reading: {http_err}')
    except Exception as err:
        print(f'Error in the resource reading: {err}')
    else:
        resource = response.json()['items']
        print(f'Resource with ID "{res_id}": {resource}')


def delete_resource(res_id: str):
    """ Deletes the resource by the resource ID
        :param res_id: ID of the resource
    """
    try:
        response = requests.delete(
            f'{url_items}/{res_id}', headers={'Authorization': f'Bearer {access_token}'}
        )
        print(f'\nDELETING THE RESOURCE with ID "{res_id}"')
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP Error at the resource deletion: {http_err}')
    except Exception as err:
        print(f'Error in the resource deletion: {err}')
    else:
        print(f'Resource with ID "{res_id}" deleted')


if __name__ == '__main__':
    authorize('test', 'test')
    resource_id = create_resource({'item': 'SOME GOODS'})
    read_resource(resource_id)
    delete_resource(resource_id)

