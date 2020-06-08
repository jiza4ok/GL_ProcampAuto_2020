import pytest
import requests
import urllib
from urllib.parse import urljoin
from classes import API, SessionUnderTest, Config, Endpoints, Helpers

# fixture to create a session under test with token refresh
# Only this fixture user for HW3 - Authentification
@pytest.fixture(scope='session')
def sessionUnderTest():
    api = API(Config.BASE_URL, Config.USERNAME, Config.PASSWORD)
    auth_responce = api.authorize()
    session = SessionUnderTest(auth_responce)
    return session

# fixture to get token for session
@pytest.fixture(scope='session')
def token():
    response = requests.post(
        urljoin(Config.BASE_URL, Endpoints.LOGIN_ENDPOINT),
        json = Helpers.login_json(Config.USERNAME, Config.PASSWORD)
    )
    return response.json()['access_token']

# fixture to create session with correct token applied
@pytest.fixture(scope='session')
def session(token):
    s = requests.Session()
    s.headers.update({'Authorization': 'Bearer {}'.format(token)})
    yield s
    s.close()
