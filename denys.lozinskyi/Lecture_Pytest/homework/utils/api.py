import requests
from requests import Response
from urllib.parse import urljoin
from ..testdata.testdata import correct_credentials
from ..config import URLs


# Joint URLs (base url with endpoints)
url_root = urljoin(URLs.base_url, URLs.root_endpoint)
url_login = urljoin(URLs.base_url, URLs.login_endpoint)
url_protected = urljoin(URLs.base_url, URLs.protected_endpoint)
url_items = urljoin(URLs.base_url, URLs.items_endpoint)


def jwt_authorize(user_name: str, password: str) -> tuple:
    """ Receives user name and user password.
        Returns the access token obtained, and the server response.
        :param user_name: user name
        :param password: user password
        :return :tuple (server_response, access_token). If token was not received its value is None
    """
    response = requests.post(url_login, json={'username': user_name, 'password': password})
    try:
        access_token = response.json()['access_token']
    except KeyError:
        return response, None
    response = requests.get(url_protected, headers={'Authorization': f'Bearer {access_token}'})
    return response, access_token


def create_resource(token: str, resource: str) -> tuple:
    """ Receives a jwt access token and a resource object to create.
        Returns an id of the resource created, and the server response.
        :param token: jwt access token
        :param resource: resource to create
        :return :tuple (server_response, resource_id). If resource creation failed, the id is None
    """
    response = requests.post(url_items, json=resource, headers={'Authorization': f'Bearer {token}'})
    try:
        # resource is (id - 1), because the server stores items in a list,
        # and makes them accessible by the index in that list. Thus, actual item id is its index
        resource_id = response.json()['id'] - 1
    except KeyError:
        return response, None
    else:
        # return resource id as a str, because the server expects resource id being str
        return response, str(resource_id)


def read_resource(token: str, resource_id: str) -> tuple:
    """ Receives a jwt access token and an id of the resource to be read.
        Returns the server response.
        :param token: jwt access token
        :param resource_id: resource id
        :return :tuple (server_response, resource_content). If resource reading failed, the resource_content is None
    """
    response = requests.get(f'{url_items}/{resource_id}', headers={'Authorization': f'Bearer {token}'})
    try:
        resource_content = response.json()['items']
    except KeyError:
        return response, None
    else:
        return response, resource_content


def delete_resource(token: str, resource_id: str) -> Response:
    """ Receives a jwt access token and an id of the resource to be deleted.
        Returns the server response.
        :param token: jwt access token
        :param resource_id: resource id
        :return :server_response
    """
    response = requests.delete(f'{url_items}/{resource_id}', headers={'Authorization': f'Bearer {token}'})
    return response


def delete_all_resources():
    """ Deletes all the resources. May be used for teardown, if needed.
        For that, authorizes with first pair of credentials taken from the test data.
    """
    credentials = correct_credentials[0]
    token = jwt_authorize(credentials['user_name'], credentials['password'])[0]
    while True:
        try:
            # since our server stores items in a list, and makes them accessible by index,
            # we can remove them all by removing zero item at every iteration
            response = delete_resource(token, "0")
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            break
    return
