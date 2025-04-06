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
    
    def add_new_row(self, datatable: Datatable, row_dict: dict):
        '''
        Given a dictionary of row data, creates a new row in the datatable
        '''
        formatted_data = {
        "attributeDataValues": row_dict
        }
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable.id}/data',
            data=formatted_data
        )
        

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
    

    #{{base_url}}/data-tables/v1/domains/{{domain_id}}/data-tables/{{datatable_id}}/queries
    def create_query(self, datatable_id, query_name, query_description):
        '''
        Given a datatable_id, query_name and query_description, creates a new query
        '''
        formatted_data = {
            "queryName": query_name,
            "queryDescription": query_description,
            "dataTableId": datatable_id
        }
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable_id}/queries',
            data=formatted_data
        )
        response = response.json()
        return response.get('queryId')
    
    #{{base_url}}/data-tables/v1/domains/{{domain_id}}/data-tables/{{datatable_id}}/queries/{{query_id}}/query-composite-filters
    def create_composite_filter(self, datatable_id, query_id, filter_type):
        '''
        Given a datatable_id, query_id, filter_type and filter_name, creates a new composite filter
        '''
        formatted_data = {
            "queryCompositeFilterType": filter_type,

        }
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable_id}/queries/{query_id}/query-composite-filters',
            data=formatted_data
        )
        response = response.json()
        return response.get('queryCompositeFilterId')
    

    '''
    {{base_url}}/data-tables/v1/domains/{{domain_id}}/data-tables/6ae142c5-eb0a-40d0-80bb-d8bc3caa1818/queries/f1e91fa6-0a7e-47c7-a686-85c3d0144254/query-composite-filters/6207eede-dd5e-43cc-bbd4-6c0dd01e2ce6/query-property-filters

    {
    "attributeId": "598f9bce-5ddc-4d76-ad7b-40f7ac41e811",
  "attributeName": "DNIS",
  "queryPropertyFilterType": "EQUAL"
}
    '''

    def create_property_filter(self, datatable_id, query_id, composite_filter_id, attribute_id, attribute_name, filter_type):
        '''
        Given a datatable_id, query_id, composite filter id, attribute_id, attribute_name and filter_type, creates a new property filter
        '''
        formatted_data = {
            "attributeId": attribute_id,
            "attributeName": attribute_name,
            "queryPropertyFilterType": filter_type
        }
        response = self.client._send_request(
            'POST',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable_id}/queries/{query_id}/query-composite-filters/{composite_filter_id}/query-property-filters',
            data=formatted_data
        )
        response = response.json()

    def get_attributes(self, datatable_id):
        '''
        Given a datatable_id, returns all attributes
        '''
        response = self.client._send_request(
            'GET',
            f'{self.DATATABLE_GET_ENDPOINT}/{datatable_id}/attributes',
        )
        response = response.json()
        return response

    def get_attribute_by_name(self, datatable_id, attribute_name):
        '''
        Given a datatable_id and attribute_name, returns the attribute
        '''
        attributes = self.get_attributes(datatable_id)
        for item in attributes['items']:
            if item['attributeName'] == attribute_name:
                return item.get('attributeId')
