from requests import Session
import base64

class BaseAPIClient:
    AUTH_ENDPOINT = '/cloudauthsvcs/v1/admin/login'

    def __init__(self, base_url):
        self.base_url = base_url
        self.params = {}
        self.headers = {'Content-Type': 'application/json'}
        self.session = Session()
        self.basic = False

    def _send_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        print(url)
        default_params = self.params.copy()
        default_params = {**default_params, **(params or {})}
        response = self.session.request(
            method, url, params=default_params, json=data, headers=self.headers)
        if response.status_code == 401:
            data = response.json()
            if data['details'][0]['code'] == 'invalid-token':
                self._refresh_token()
                # Let's retry the failed request
                # I think this is a never ending loop, need to fix..
                # in fact commenting out untill better solution
                # return self._send_request(method, endpoint, params, data)
                return False

        if response.status_code > 299:
            raise Exception(
                f'Request failed with status code {response.status_code} {response}')
        return response

    def _refresh_token(self):
        self._set_token_in_param(self._get_token(
            self.username, self.password))

    def _get_token(self, username, password):
        payload = {
            'userName': username,
            'password': password
        }
        response = self.session.post(
            f'{self.base_url}{self.AUTH_ENDPOINT}',
            json=payload)
    
        # Validatde the response
        if response.status_code != 200:
            raise Exception(
                f'Auth request failed witrh status code {response.status_code} {response.json()}')
        data = response.json()
        return data['access_token']

    def _set_token_in_param(self, access_token):
        self.headers['Authorization'] = f'Bearer {access_token}'
    
    def _get_basic_auth(self):
        self.basic = True
        return base64.b64encode(f'{self.username}:{self.password}'.encode()).decode()
    
    def _set_basic_auth(self):
        self.headers['Authorization'] = f'Basic {self._get_basic_auth()}'
    
