from requests import Session
from requests.auth import HTTPDigestAuth
import base64
from enum import Enum
from abc import ABC,  abstractmethod


class AuthStrategy(ABC):
    @abstractmethod
    def authenticate(self, client):
        pass

    @abstractmethod
    def refresh(self, client):
        pass


class Five9ApiType(Enum):
    STUDIO_V6 = 'studio_v6'
    STUDIO_V7 = 'studio_v7'
    VCC_CLASSIC = 'vcc_classic'
    VCC_CLOUD = 'vcc_cloud'


class BasicAuthStrategy(AuthStrategy):
    def authenticate(self, client):
        basic_auth = base64.b64encode(
            f'{client.username}:{client.password}'.encode()
        ).decode()
        client.headers['Authorization'] = f'Basic {basic_auth}'
    
    def refresh(self, client):
        self.authenticate(client)


class AdminConsoleAuthStrategy(AuthStrategy):
    def authenticate(self, client):
        token = self._get_token(client)
        client.headers['Authorization'] = f'Bearer {token}'
    
    def _get_token(self, client):
        response = client.session.post(
            f'{client.base_url}{client.AUTH_ENDPOINT}',
            json={
                'userName': client.username,
                'password': client.password
            }
        )
        return response.json()['access_token']


class Studio6AuthStrategy(AuthStrategy):
    def authenticate(self, client):
        token = self._get_token(client)
        client.params['token'] = token
    
    def _get_token(self, client):
        response = client.session.post(
            f'{client.base_url}{client.AUTH_ENDPOINT}',
            auth=HTTPDigestAuth(client.username, client.password),
            params={'apikey': client.api_key}
        )
        return response.json()['result']['token']
    
    def refresh(self, client):
        self.authenticate(client)


class Studio7AuthStrategy(AuthStrategy):
    def authenticte(self, client):
        client.headers['studio-api-key'] = client.api_key


class AuthStrategyFactory:
    @staticmethod
    def create_Strategy(api_type: Five9ApiType) -> AuthStrategy:
        strategies = {
            Five9ApiType.STUDIO_V6: Studio6AuthStrategy(),
            Five9ApiType.STUDIO_V7: Studio7AuthStrategy(),
            Five9ApiType.VCC_CLASSIC: BasicAuthStrategy(),
            Five9ApiType.VCC_CLOUD: AdminConsoleAuthStrategy()
        }
        return strategies[api_type]