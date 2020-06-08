import pytest
import requests
import urllib
from urllib.parse import urljoin
import jwt
import datetime
import time

class Config:
    BASE_URL = "http://localhost:5002/"
    USERNAME = 'test'
    PASSWORD = 'test'
    NEW_ITEM_JSON = {'item': 'newItem'}

class Endpoints:
    ITEMS_ENDPOINT = '/items'
    LOGIN_ENDPOINT = '/login'
    PROTECTED_ENDPOINT = '/protected'
    REFRESH_ENPOINT = '/refresh'

class Helpers:
    @staticmethod
    def login_json(user, password):
        json = {'username': user, 'password': password}
        return json

    # join 3 parts of URL: <base_url>/<endpoint>/<resource_id>
    @staticmethod
    def url_join(base_url, endpoint, resource_id):
        return urljoin(base_url, endpoint + '/' + str(resource_id))

    # get created item_id from create (POST) request
    @staticmethod
    def item_id(response):
        return response.json()['id']-1  # -1 => because of bug in symple-app.py 

class API:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def authorize(self):
        response = requests.post(
            urljoin(self.url, Endpoints.LOGIN_ENDPOINT),
            json = Helpers.login_json(self.user, self.password)
        )
        return response

    def login(self, session):
        url = urljoin(self.url, Endpoints.PROTECTED_ENDPOINT)
        return session.get(url)

    def add_item(self, session):
        url = urljoin(self.url, Endpoints.ITEMS_ENDPOINT)
        return session.post(url, json = Config.NEW_ITEM_JSON)

    def request_item(self, session, id):
        url = Helpers.url_join(self.url, Endpoints.ITEMS_ENDPOINT, id)
        return session.get(url)

    def remove(self, session, id):
        url = Helpers.url_join(self.url, Endpoints.ITEMS_ENDPOINT, id)
        return session.delete(url)

class SessionUnderTest:
    def __init__(self, auth_responce):
        self.access_token = self.get_tokens(auth_responce)['access_token']
        self.refresh_token = self.get_tokens(auth_responce)['refresh_token']

    def get_tokens(self, response):
        try:
            access_token = response.json()['access_token']
        except:
            print("Cannot get Access token from response") 
        try:        
            refresh_token = response.json()['refresh_token']
        except:
            print("Cannot get Refresh token from response") 
        return dict(access_token = access_token, refresh_token = refresh_token)

    def get_decoded_token(self, access_token):
        try:
            decoded_access_token = jwt.decode(self.access_token, verify=False)
            return decoded_access_token
        except:
            print("Cannot decode Access token")
            
    def is_token_alive(self):
        decoded_token = self.get_decoded_token(self.access_token)
        token_exp_date = decoded_token['exp']
        current_datetime = datetime.datetime.now().timestamp()
        return token_exp_date > current_datetime

    def renew_access_token(self):
        response = requests.post(
            urljoin(Config.BASE_URL, Endpoints.REFRESH_ENPOINT),
            headers={"Authorization": f"Bearer {self.refresh_token}"}
        )
        self.access_token = response.json()['access_token']
        return self.access_token
