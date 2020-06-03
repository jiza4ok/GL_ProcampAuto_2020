import requests
import jwt  
import datetime
import urlparse


class ENDPOINTS:
    ITEMS = '/items'
    LOGIN = '/login'
    REFRESH = '/refresh'

class BaseAPI:

    def __init__(self, session):
        self.session = session

    def get(self):
        pass

    def post(self):
        pass


class Session:

    def init(self, access_token, refresh_token, config):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self.config = config

    @property
    def access_token(self):
        try:
            return jwt.decode(self._access_token)
        except:
            print('Decoding jwt failed.')
    
    @property
    def headers(self):
        return {"Authorization": f"Bearer {self._access_token}"}

    def build_url(self, url):
        return urlparse.urljoin(self.config['base_url'], url)

    def is_expired(self):
        return self.access_token['exp'] <= datetime.datetime.now()

    def renew(self):
        r = requests.post(url=self.build_url(ENDPOINTS.REFRESH), headers={"Authorization": f"Bearer {self._refresh_token}"})
        r.raise_for_status()
        
        self._access_token = r['access_token']
        return self.access_token


class API:  
  
    def init(self, username, password, config):
        self.username = username
        self.password = password
        self.config = config
        
        self.session = None

    def build_url(self, url):
        return urlparse.urljoin(self.config['base_url'], url)

    def login(self):
        r = requests.post(url=self.build_url(ENDPOINTS.LOGIN), json=dict(username='test', password='test'))
        r.raise_for_status()

        self.session = Session(**r)

    def get_item(self):
        if self.session.is_expired():
            self.session.renew()

        requests.get(url=self.build_url(ENDPOINTS.ITEMS), headers=self.session.headers)        
 
