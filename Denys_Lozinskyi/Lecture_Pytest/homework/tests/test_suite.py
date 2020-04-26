import os
import signal
import requests
import pytest
from requests import HTTPError
from subprocess import Popen
from ..testdata import testdata
from time import sleep


# Run pytest from the "Lecture_Pytest$" folder

link_to_server = 'homework/server/simple-app.py'
server_run = f"python3 {link_to_server}"


@pytest.fixture(scope='session', params=testdata.correct_credentials)
def positive_test_case(request):
    process = Popen(server_run, shell=True, preexec_fn=os.setsid)
    # give the server a few seconds to start
    sleep(2)
    yield request.param
    os.killpg(process.pid, signal.SIGTERM)


@pytest.fixture(params=testdata.incorrect_credentials)
def negative_test_case(request):
    testdata.access_token = ''
    return request.param


@pytest.mark.smoke
def test_authorization(positive_test_case):
    # obtaining access token with the credentials given
    user_name, password = positive_test_case['user_name'], positive_test_case['password']
    response_1 = requests.post(testdata.url + 'login', json={'username': user_name, 'password': password})
    testdata.access_token = response_1.json()['access_token']
    assert len(testdata.access_token) > 0, "Token not received"

    # logging in with the access token received
    response_2 = requests.get(testdata.url + 'protected', headers={'Authorization': f'Bearer {testdata.access_token}'})
    assert 200 <= response_2.status_code < 300
    assert response_2.json() == {'logged_in_as': user_name}


def test_resource_creation(positive_test_case):
    response = requests.post(
        testdata.url + 'items', json=testdata.resources[0], headers={'Authorization': f'Bearer {testdata.access_token}'}
    )
    assert 200 <= response.status_code < 300
    testdata.resource_id = str(response.json()['id'] - 1)


def test_resource_reading(positive_test_case):
    response = requests.get(
        testdata.url + f'items/{testdata.resource_id}', headers={'Authorization': f'Bearer {testdata.access_token}'}
    )
    assert 200 <= response.status_code < 300


def test_resource_deletion(positive_test_case):
    response = requests.delete(
        testdata.url + f'items/{testdata.resource_id}', headers={'Authorization': f'Bearer {testdata.access_token}'}
    )
    assert 200 <= response.status_code < 300
    with pytest.raises(HTTPError):
        response = requests.delete(
            testdata.url + f'items/{testdata.resource_id}', headers={'Authorization': f'Bearer {testdata.access_token}'}
        )
        response.raise_for_status()


def test_authorization_with_wrong_credentials(negative_test_case):
    # attempting to obtain access token with the credentials given
    user_name, password = negative_test_case['user_name'], negative_test_case['password']
    response_1 = requests.post(testdata.url + 'login', json={'username': user_name, 'password': password})
    with pytest.raises(KeyError):
        testdata.access_token = response_1.json()['access_token']

    # attempting to log in
    response_2 = requests.get(testdata.url + 'protected', headers={'Authorization': f'Bearer {testdata.access_token}'})
    with pytest.raises(AssertionError):
        assert 200 <= response_2.status_code < 300
    with pytest.raises(AssertionError):
        assert response_2.json() == {'logged_in_as': user_name}
