from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator


class Attribute(BaseModel):
    '''
    Represents a data table attribute, which is a column in a data table.
    '''
    datatable_id: str = Field(alias='dataTableId')
    id: str = Field(alias='attributeId')
    name: str = Field(alias='attributeName')
    data_type: str = Field(alias='dataType')
    uri: Optional[str] = None
    default_value: Optional[str] = Field(alias='attributeDefaultValue')
    min_value: Optional[str] = Field(alias='attributeMinimumValue')
    max_value: Optional[str] = Field(alias='attributeMaximumValue')
    unique: Optional[bool] = None
    required: Optional[bool] = None
    contains_sensitive_data: Optional[bool] = Field(
        alias='containsSensitiveData')

    @validator('data_type')
    def validate_data_type(cls, value):
        valid_data_types = {'STRING', 'INTEGER_64_BIT',
                            'DECIMAL_64_BIT', 'BOOLEAN', 'TIMESTAMP'}
        if value not in valid_data_types:
            raise ValueError(f'Invalid data type: {value}')
        return value



class Datatable(BaseModel):
    '''
    Represents a data table object.

    Attributes:
        id (str): The ID of the data table.
        name (str): The name of the data table.
        description (str): The description of the data table.
        uri (str): The URI of the data table.
        row_count (int, optional): The number of rows in the data table.
    '''

    id: Optional[str] = Field(None, alias='dataTableId')
    name: str = Field(alias='dataTableName')
    description: str = Field(alias='dataTableDescription')
    uri: Optional[str] = None
    row_count: Optional[int] = Field(None, alias='rowCount')
    attributes: List[Attribute] = []

    def get_attribute_by_name(self, name: str) -> Attribute:
        '''
        Returns the attribute with the given name.
        '''
        for attr in self.attributes:
            if attr.name == name:
                return attr
        raise ValueError(f'Attribute with name {name} does not exist')


class Row(BaseModel):
    '''
    Represents a row in a data table.
    '''
    datatable: Datatable
    data: Dict[str, Any] = Field(serialization_alias='attributeDataValues')

    @validator('data')
    def validate_data_keys_match_attributes(cls, data, values):
        datatable: Datatable = values.get('datatable')
        if not datatable:
            raise ValueError('Datatable is required to validate row data')
        attribute_names = {attr.name for attr in datatable.attributes}
        if not set(data.keys()).issubset(attribute_names):
            raise ValueError('Row data keys do not match datatable attributes')
        return data


class Query(BaseModel):
    '''
    Represents a user defined query for a particular datatable.
    '''
    id: Optional[str] = Field(alias='queryId')
    name: str = Field(alias='queryName')
    datatable_id: str = Field(alias='dataTableId')
    description: str = Field(alias='queryDescription')
    order_by_attribute: Optional[str] = Field(
        serialization_alias='orderByAttribute')
    order_by_sort_type: Optional[str] = Field(
        serialization_alias='orderBySortType')
    row_limit: Optional[int] = Field(serialization_alias='rowLimit')
    uri: Optional[str] = None


class QueryCompositeFilter(BaseModel):
    '''
    Represents a composite filter for a query.
    '''
    id: Optional[str] = Field(serialization_alias='queryCompositeFilterId')
    type: str = Field(serialization_alias='queryCompositeFilterType')
    parent: Optional[str] = Field(
        serialization_alias='queryCompositeFilterParent')
