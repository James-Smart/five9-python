from functools import partial
from requests.auth import HTTPDigestAuth
import requests
import json
from ..models.query_filter import Filter
from .base_client import BaseAPIClient
from .v6_tasks import StudioV6Tasks
from .v6_prompts import StudioV6Prompts
from .v6_datastores import StudioV6Datatstores


class StudioAPIClientV6(BaseAPIClient, StudioV6Tasks, StudioV6Prompts, StudioV6Datatstores):
    """A python interface to the Five9 Studio 6 Datatstore API."""

    AUTH_ENDPOINT = '/portal/api/v2/auth/get-token'
    DATASOTRE_LIST_ENDPOINT = '/studio_instance/studio-api/v1/datastore/list-all'
    DATASTORE_LIST_ONE_ENDPOINT = '/studio_instance/studio-api/v1/datastore/list-one-row'
    GET_AUDIO_FILE_ENDPOINT = '/studio_instance/studio-api/v1/datastore/get-audio-file'
    DATASTORE_SEARCH_ENDPOINT = '/studio_instance/studio-api/v1/datastore/search'

    def __init__(self, base_url, username, password, api_key, max_requests_per_second=5):
        """Instantiate a new StudioAPIClientV6 object.

        Args:
            base_url (str): The base URL of the Studio instance.
            username (str): The username of the Studio user.
            password (str): The password of the Studio user (taken from the api docs, not login).
            api_key (str): The API key of the Studio user.
            max_requests_per_second (int, optional): The maximum number of requests per second. Defaults to 5.

        """
        super().__init__(base_url, max_requests_per_second)
        self.api_key = api_key
        self.headers = {'Content-Type': 'application/json'}
        self.username = username
        self.password = password
        self._set_token_in_param(
            self._get_token(username, password, api_key))

    def _refresh_token(self):
        self._set_token_in_param(self._get_token(
            self.username, self.password, self.api_key))

    def _get_token(self, username, password, api_key):
        response = requests.post(
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
