import datetime
import time

import jwt
import requests


class BaseAPI:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()
        self.server = None

    def login(self, server: str, login: str, passw: str):
        response = self.session.post(server + '/login', json={'username': login, 'password': passw})
        response.raise_for_status()
        self.server = server
        self.access_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']

    def get_tokens(self):
        return self.access_token, self.refresh_token

    def renew(self):
        response = self.session.post(self.server + '/refresh', headers={"Authorization": f"Bearer {self.refresh_token}"})
        response.raise_for_status()
        self.access_token = response.json()['access_token']
        return self.access_token

    def create_item(self, item):
        response = self.session.post(self.server + '/items', json=item, headers={"Authorization": f"Bearer {self.access_token}"})
        response.raise_for_status()
        res_id = response.json()['id'] - 1
        print(f'Resource "{item}" is created with ID: "{res_id}"')
        return res_id

    def read_item(self, id: int):
        response = self.session.get(self.server + '/items/' + str(id), headers={"Authorization": f"Bearer {self.access_token}"})
        response.raise_for_status()
        return response.json()['items']

    def read_items(self):
        response = self.session.get(self.server + '/items', headers={"Authorization": f"Bearer {self.access_token}"})
        response.raise_for_status()
        return response.json()['items']

    def delete_item(self, id: int):
        response = self.session.delete(self.server + '/items/' + str(id), headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return response.status_code == 200

    def close_connection(self):
        self.session.close()


baseApi = BaseAPI()
baseApi.login('http://localhost:5002', 'test', 'test')
tokens = baseApi.get_tokens()
print(tokens)
#print(baseApi.renew())
#print()
#tokens = baseApi.get_tokens()
#print(tokens)

#print(baseApi.create_item(123))
#print(baseApi.read_items())
#print(baseApi.delete_item(0))
#print(baseApi.read_items())
#baseApi.close_connection()

print(jwt.decode(tokens[0], verify=False)['exp'])
print(int(time.time()))
time.sleep(40)


expiration_time = jwt.decode(baseApi.get_tokens()[0], verify=False)['exp']
if expiration_time < int(time.time()):
   baseApi.renew()
   print("RENEWIG TOKEN")

#tokens = baseApi.get_tokens()
#print(tokens)
#baseApi.close_connection()