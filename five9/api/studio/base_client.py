from requests.auth import HTTPDigestAuth
from requests_ratelimiter import LimiterSession


class BaseAPIClient:
    AUTH_ENDPOINT = '/portal/api/v2/auth/get-token'

    def __init__(self, base_url, max_requests_per_second=5):
        self.base_url = base_url
        self.params = {}
        # self._rate_limiter = RateLimiter(
        #    max_calls=max_requests_per_second, period=1)
        self.session = LimiterSession(per_second=max_requests_per_second)

    @property
    def rate_limiter(self):
        return self._rate_limiter

    def _send_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        default_params = self.params.copy()
        default_params = {**default_params, **(params or {})}
        response = self.session.request(
            method, url, params=default_params, json=data)
        if response.status_code == 400:
            data = response.json()
            if data['result']['error']['code'] == 'INVALID_TOKEN':
                self._refresh_token()
                # Let's retry the failed request
                # I think this is a never ending loop, need to fix..
                # in fact commenting out untill better solution
                # return self._send_request(method, endpoint, params, data)
                return False

        if response.status_code != 200:
            raise Exception(
                f'Request failed with status code {response.status_code} {response.json()}')
        return response

    def _refresh_token(self):
        self._set_token_in_param(self._get_token(
            self.username, self.password, self.api_key))

    def _get_token(self, username, password, api_key):
        response = self.session.post(
            f'{self.base_url}{self.AUTH_ENDPOINT}',
            auth=HTTPDigestAuth(username, password),
            params={'apikey': api_key})

        # Validatde the response
        if response.status_code != 200:
            raise Exception(
                f'Auth request failed witrh status code {response.status_code}')
        data = response.json()
        return data['result']['token']

    def _set_token_in_param(self, token):
        self.params['token'] = token
