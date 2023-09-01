from functools import partial
from requests.auth import HTTPDigestAuth
import requests
import json
from ..models.query_filter import Filter
from .base_client import BaseAPIClient
from .v6_tasks import StudioV6Tasks
from .v6_prompts import StudioV6Prompts


class StudioAPIClientV6(BaseAPIClient, StudioV6Tasks, StudioV6Prompts):
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

    def get_datastore_id(self, datastore_name):
        """Get the datastore ID for a given datastore name.

        Args:
            datastore_name (str): The name of the datastore.
        """
        response = self._send_request(
            'POST',
            self.DATASOTRE_LIST_ENDPOINT,

        )

        datastores = response.json().get('result', [])
        for datastore in datastores:
            if datastore['name'] == datastore_name:
                return datastore['id']

        raise Exception(
            f'Could not find datastore with name {datastore_name}.')

    def get_datastore_row_byid(self, datastore_id, row_id):
        """Get a single row from a datastore by ID.

        Args:
            datastore_id (str): The ID of the datastore.
            row_id (int): The ID of the row.
        """
        params = {
            'datastore_id': datastore_id,
            'data_id': row_id
        }
        response = self._send_request(
            'POST',
            self.DATASTORE_LIST_ONE_ENDPOINT,
            params=params,
            data={'datastoreId': datastore_id, 'rowId': row_id}
        )
        return response.json().get('result', {})

    def get_datastore_audio_file(self, datastore_id, row_id, column_name):
        """Get the audio file for a given row and column.

        Args:
            datastore_id (str): The ID of the datastore.
            row_id (int): The ID of the row.
            column_name (str): The name of the column.
        """
        params = {
            'datastore_id': datastore_id,
            'data_id': row_id,
            'column_name': column_name
        }
        response = self._send_request(
            'POST',
            self.GET_AUDIO_FILE_ENDPOINT,
            params=params,
            data={'datastoreId': datastore_id, 'rowId': row_id}
        )
        return response.content

    def get_datastore_search_rows(self, datastore_id, filters=None):
        """Get a list of rows from a datastore that match the given filters.

        Args:
            datastore_id (str): The ID of the datastore.
            filters (list, optional): A list of filters to apply to the search. Defaults to None.
        """
        base_params = {
            'datastore_id': datastore_id
        }

        if filters:
            for i, filter_obj in enumerate(filters):
                base_params.update(filter_obj.to_params(i))

        response = self._send_request(
            'POST',
            self.DATASTORE_SEARCH_ENDPOINT,
            params=base_params,
            data={}
        )

        return response.json().get('result', [])
