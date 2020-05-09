import pytest
import requests
from global_scope import base_url
from homework.rest.api_pathes import login

class Authorization:

    @pytest.fixture(scope="function")
    def authorization_and_get_token(self):
        response = requests.post(
            base_url + login,
            json={'username': 'test', 'password': 'test'}
        )
        yield response
        # token = response.json()['access_token']
        # print(f'Token: {token}\n')
        # yield token