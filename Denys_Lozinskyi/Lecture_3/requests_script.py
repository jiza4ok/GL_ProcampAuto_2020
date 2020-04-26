#! /usr/bin/python3.7
import requests
from requests.auth import HTTPBasicAuth


def get_working_with():

    response_0 = requests.get('http://0.0.0.0:5002/')
    response_1 = requests.get('http://0.0.0.0:5002/fail500')
    response_2 = requests.get('http://0.0.0.0:5002/users')

    print(response_0.__dict__)
    print(f'Response, status code: {response_0.status_code}')
    print(f'Response 1, status code: {response_1.status_code}')
    print(f'Response 2, status code: {response_2.status_code}')
    print(response_0.json())


def post_working_with():

    response = requests.post(
        'http://0.0.0.0:5002/',
        json={'serbut': 'value'}
    )
    json_response = response.json()
    print(f'Response: {json_response}')


def auth_working_with():
    response = requests.get(
        'http://0.0.0.0:5002/basic_auth',
        auth=HTTPBasicAuth('sergii', 'hello')
    )
    print(response.text)


def jwc_auth_working_with():
    response = requests.post(
        'http://0.0.0.0:5002/login',
        json={'username': 'test', 'password': 'test'}
    )
    # print(response.json())
    access_token = response.json()['access_token']
    print(f'Token: {access_token}')
    return access_token


def jwc_auth2_working_with(token):

    url = 'http://0.0.0.0:5002/protected'
    response = requests.get(url)

    print('Sending unauthorized request')
    print(response.text)

    print('Sending Authorized request')
    response = requests.get(
        url, headers={'Authorization': f"Bearer {token}"}
    )
    print(response.text)


# get_working_with()
post_working_with()
# auth_working_with()
# jwc_auth_working_with()
# jwc_auth2_working_with(jwc_auth_working_with())

