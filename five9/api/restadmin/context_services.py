from ...models.context_services_model import Datatable, Attribute, Row


class ContextServices:

    def __init__(self, client):
        self.client = client
        self.DATATABLE_GET_ENDPOINT = f'/data-tables/v1/domains/{self.client.domain_id}/data-tables'

    def add_datatable(self, datatable: Datatable) -> Datatable:
        '''
        Given a datatable, creates a new datatable
        '''
        response = self.client._send_request(
            'POST',
            self.DATATABLE_GET_ENDPOINT,
            data=datatable.model_dump(
                by_alias=True, exclude_none=True, exclude_defaults=True)
        )
        datatable = Datatable.model_validate(response.json())
        return datatable

    def get_datatable_by_name(self, datastore_name):
        """Get the datastore ID for a given datastore name.

        Args:
            datastore_name (str): The name of the datastore.
        """
        response = self.client._send_request(
            'GET',
            self.DATATABLE_GET_ENDPOINT,

        )

        datastores = response.json().get('items', [])
        for datastore in datastores:
            if datastore['dataTableName'] == datastore_name:
                return Datatable.model_validate(datastore)
                # return datastore['dataTableId']

        raise Exception(
            f'Could not find datastore with name {datastore_name}.')

    def get_attibutes(self, datatable: Datatable) -> Datatable:
        """Get the datastore ID for a given datastore name.

        Args:
            datatable (Datatable): The name of the datastore.
        """
        response = self.client._send_request(
            'GET',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable.id}/attributes',

        )
        # datatable.attributes = response.json().get('items', [])
        datatable.attributes = [Attribute.model_validate(
            attr) for attr in response.json().get('items', [])]
        return datatable

    def update_attribute(self, attribute: Attribute) -> Attribute:
        '''
        Given an attribute, updates the changed fields
        '''
        response = self.client._send_request(
            'PUT',
            f'{self.DATATABLE_GET_ENDPOINT}/{attribute.datatable_id}/attributes/{attribute.id}',
            data=attribute.model_dump(
                by_alias=True, exclude_none=True)
        )
        attribute = Attribute.model_validate(response.json())
        return

    def add_attribute(self, attribute: Attribute) -> Attribute:
        '''
        Given an attribute, updates the changed fields
        '''
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{attribute.datatable_id}/attributes',
            data=attribute.model_dump(
                by_alias=True, exclude_none=True)
        )
        attribute = Attribute.model_validate(response.json())
        return attribute

    def delete_attribute(self, attribute: Attribute) -> Attribute:
        '''
        Given an attribute, updates the changed fields
        '''
        response = self.client._send_request(
            'DELETE',
            f'{self.DATATABLE_GET_ENDPOINT}/{attribute.datatable_id}/attributes/{attribute.id}'
        )
        if response.status_code != 204:
            raise Exception(f'Failed to delete attribute {attribute.name}')
        return True

    def add_row(self, row: Row) -> Row:
        '''
        Given a row, updates the changed fields
        '''
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{row.datatable.id}/data',
            data=row.model_dump(
                by_alias=True, exclude_none=True, exclude={'datatable'})
        )
        row = Row(data=response.json().get(
            'attributeDataValues', {}), datatable=row.datatable)
        return row
