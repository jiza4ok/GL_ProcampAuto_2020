import os
import signal
import requests
import pytest
from requests import HTTPError
from subprocess import Popen
from ..testdata import testdata
from time import sleep


# Run Pytest from the "Lecture_Pytest" folder

link_to_server = 'homework/server/simple-app.py'
server_run = f"python3 {link_to_server}"


@pytest.fixture(scope='session')
def session_fixture():
    """ SETUP: runs the test server at the start of the session;
        TEARDOWN: stops it as the session concludes """
    process = Popen(server_run, shell=True, preexec_fn=os.setsid)
    # give the server a few seconds to start
    # (NB! need to find a way to read a signal from the server saying it's started, and replace 'sleep' with it)
    sleep(2)
    yield
    os.killpg(process.pid, signal.SIGTERM)


@pytest.fixture(params=testdata.correct_credentials)
def authorization_positive(request):
    """ use as a SETUP for tests require preliminary authorization with access token """
    user_name, password = request.param['user_name'], request.param['password']
    response_1 = requests.post(testdata.url + 'login', json={'username': user_name, 'password': password})
    testdata.access_token = response_1.json()['access_token']
    assert len(testdata.access_token) > 0, "Token not received"
    # logging in with the access token received
    response_2 = requests.get(testdata.url + 'protected', headers={'Authorization': f'Bearer {testdata.access_token}'})
    assert 200 <= response_2.status_code < 300
    assert response_2.json() == {'logged_in_as': user_name}
    yield


@pytest.fixture(params=testdata.incorrect_credentials)
def authorization_negative(request):
    """ use as a setup for negative tests. Provides them with incorrect credentials from testdata """
    testdata.access_token = ''
    yield request.param


@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.parametrize('credentials', (testdata.correct_credentials[0],))
def test_authorization(session_fixture, credentials):
    """ a standalone test verifying authorization with one pair of correct credentials.
        Can be run within the scope of the session
    """
    url = testdata.url
    user_name, password = credentials['user_name'], credentials['password']
    # obtaining access token with the credentials given
    response_1 = requests.post(url + 'login', json={'username': user_name, 'password': password})
    access_token = response_1.json()['access_token']
    assert len(access_token) > 0, 'Token not received'
    # logging in with the access token received
    response_2 = requests.get(url + 'protected', headers={'Authorization': f'Bearer {access_token}'})
    assert 200 <= response_2.status_code < 300
    assert response_2.json() == {'logged_in_as': user_name}


@pytest.mark.positive
def test_resource_creation(session_fixture, authorization_positive):
    """ verifies that a resource can be created given a proper token obtained after authorization """
    url, access_token, resource = testdata.url, testdata.access_token, testdata.resources[0]
    response_1 = requests.post(
        url + 'items', json=resource, headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 200 <= response_1.status_code < 300
    testdata.resource_id.append(str(response_1.json()['id'] - 1))
    response_2 = requests.get(
        url + f'items/{testdata.resource_id[-1]}', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 200 <= response_2.status_code < 300
    assert response_2.json()['items'] == resource


@pytest.mark.positive
def test_resource_reading(session_fixture, authorization_positive):
    """ verifies that a resource can be read by its ID given a proper token obtained after authorization """
    url, access_token, resource_id = testdata.url, testdata.access_token, testdata.resource_id
    response = requests.get(
        testdata.url + f'items/{resource_id[-1]}', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 200 <= response.status_code < 300


@pytest.mark.positive
def test_resource_deletion(session_fixture, authorization_positive):
    """ verifies a resource can be deleted by its ID given a proper token obtained after authorization """
    url, access_token, resource_id = testdata.url, testdata.access_token, testdata.resource_id
    response = requests.delete(
        url + f'items/{resource_id[-1]}', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 200 <= response.status_code < 300
    with pytest.raises(HTTPError):
        response = requests.delete(
            url + f'items/{resource_id[-1]}', headers={'Authorization': f'Bearer {access_token}'}
        )
        response.raise_for_status()
    testdata.resource_id.pop(-1)


@pytest.mark.negative
def test_authorization_with_wrong_credentials(session_fixture, authorization_negative):
    """ verifies impossibility to receive an access token and authorize with incorrect creds """
    user_name, password = authorization_negative['user_name'], authorization_negative['password']
    url, access_token = testdata.url, None
    response_1 = requests.post(url + 'login', json={'username': user_name, 'password': password})
    with pytest.raises(KeyError):
        access_token = response_1.json()['access_token']
    # attempting to log in
    response_2 = requests.get(url + 'protected', headers={'Authorization': f'Bearer {access_token}'})
    with pytest.raises(HTTPError):
        response_2.raise_for_status()
    with pytest.raises(AssertionError):
        assert response_2.json() == {'logged_in_as': user_name}


@pytest.mark.negative
@pytest.mark.parametrize('token', (None, '', ' '))
def test_resource_creation_with_no_token(session_fixture, token):
    """ verifies impossibility to create a resource with no access token """
    url, access_token = testdata.url, token
    response = requests.post(
        url + 'items', json=testdata.resources[0], headers={'Authorization': f'Bearer {access_token}'}
    )
    with pytest.raises(HTTPError):
        response.raise_for_status()
