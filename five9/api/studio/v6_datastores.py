class StudioV6Datatstores():
    DATASTORE_LIST_ENDPOINT = '/studio_instance/studio-api/v1/datastore/list-all'
    DATASTORE_LIST_ONE_ENDPOINT = '/studio_instance/studio-api/v1/datastore/list-one-row'
    GET_AUDIO_FILE_ENDPOINT = '/studio_instance/studio-api/v1/datastore/get-audio-file'
    DATASTORE_SEARCH_ENDPOINT = '/studio_instance/studio-api/v1/datastore/search'

    def __init__(self, client):
        self.client = client

    def get_datastore_id(self, datastore_name):
        """Get the datastore ID for a given datastore name.

        Args:
            datastore_name (str): The name of the datastore.
        """
        response = self.client._send_request(
            'POST',
            self.DATASTORE_LIST_ENDPOINT,

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
        response = self.client._send_request(
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
        response = self.client._send_request(
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

        response = self.client._send_request(
            'POST',
            self.DATASTORE_SEARCH_ENDPOINT,
            params=base_params,
            data={}
        )

        return response.json().get('result', [])
