from ...models.cav import (
    Variable, 
    VariableGroup, 
    VariableGroupListResponse, 
    VariableListResponse
)


class CAV:
    """
    Client for interacting with the Custom Agent Verification (CAV) API.
    
    CAVs are variables that exist within containers called variable groups.
    Both system and user-defined 'custom' variable/variable groups can exist.
    This class provides methods to create, retrieve, and update both variable
    groups and variables (CAVs).
    """

    def __init__(self, client):
        """
        Initialize the CAV client.
        
        Args:
            client: The base client for making API requests.
        """
        self.client = client
        self.VARIABLE_GROUP_ENDPOINT = f'/interactions/v1/domains/{self.client.domain_id}/variable-groups'
        self.VARIABLE_ENDPOINT = f'/interactions/v1/domains/{self.client.domain_id}/variables'

    def get_variable_groups(self) -> VariableGroupListResponse:
        """
        Get all variable groups.
        
        Returns:
            VariableGroupListResponse: A list of variable group objects.
        """
        response = self.client._send_request(
            'GET',
            self.VARIABLE_GROUP_ENDPOINT
        )
        return VariableGroupListResponse.model_validate(response.json())

    def get_variable_group_by_id(self, variable_group_id: str) -> VariableGroup:
        """
        Get a variable group by ID.
        
        Args:
            variable_group_id (str): The ID of the variable group.
            
        Returns:
            VariableGroup: The variable group object.
            
        Raises:
            Exception: If the variable group is not found.
        """
        response = self.client._send_request(
            'GET',
            f'{self.VARIABLE_GROUP_ENDPOINT}/{variable_group_id}'
        )
        return VariableGroup.model_validate(response.json())

    def get_variable_group_by_name(self, name: str) -> VariableGroup:
        """
        Get a variable group by name.
        
        Args:
            name (str): The name of the variable group.
            
        Returns:
            VariableGroup: The variable group object.
            
        Raises:
            Exception: If the variable group is not found.
        """
        variable_groups = self.get_variable_groups()
        for group in variable_groups.items:
            if group.name == name:
                return group
        raise Exception(f'Could not find variable group with name {name}.')

    def create_variable_group(self, variable_group: VariableGroup) -> VariableGroup:
        """
        Create a new variable group.
        
        Args:
            variable_group (VariableGroup): The variable group to create.
            
        Returns:
            VariableGroup: The created variable group object.
        """
        response = self.client._send_request(
            'POST',
            self.VARIABLE_GROUP_ENDPOINT,
            data=variable_group.model_dump(
                by_alias=True, exclude_none=True, exclude_defaults=True)
        )
        return VariableGroup.model_validate(response.json())

    def update_variable_group(self, variable_group: VariableGroup) -> VariableGroup:
        """
        Update an existing variable group.
        
        Args:
            variable_group (VariableGroup): The variable group to update.
            
        Returns:
            VariableGroup: The updated variable group object.
        """
        if not variable_group.variable_group_id:
            raise ValueError("Variable group ID is required for update operation")
            
        response = self.client._send_request(
            'PUT',
            f'{self.VARIABLE_GROUP_ENDPOINT}/{variable_group.variable_group_id}',
            data=variable_group.model_dump(
                by_alias=True, exclude_none=True, exclude_defaults=True)
        )
        return VariableGroup.model_validate(response.json())

    def delete_variable_group(self, variable_group_id: str) -> bool:
        """
        Delete a variable group.
        
        Args:
            variable_group_id (str): The ID of the variable group to delete.
            
        Returns:
            bool: True if deletion was successful.
            
        Raises:
            Exception: If deletion fails.
        """
        response = self.client._send_request(
            'DELETE',
            f'{self.VARIABLE_GROUP_ENDPOINT}/{variable_group_id}'
        )
        if response.status_code != 204:
            raise Exception(f'Failed to delete variable group {variable_group_id}')
        return True

    def get_variables(self, variable_group_id: str = None, page_limit: int = 100) -> VariableListResponse:
        """
        Get all variables, optionally filtered by variable group ID.
        
        Args:
            variable_group_id (str, optional): The ID of the variable group to filter by.
            page_limit (int, optional): The maximum number of variables to return.
            
        Returns:
            VariableListResponse: A list of variable objects.
        """
        url = self.VARIABLE_ENDPOINT
        params = {'pageLimit': page_limit, 'sort': 'name'}
        
        if variable_group_id:
            params['filter'] = f'variableGroup.variableGroupId=={variable_group_id}'
            
        response = self.client._send_request(
            'GET',
            url,
            params=params
        )
        return VariableListResponse.model_validate(response.json())

    def get_variable_by_id(self, variable_id: str) -> Variable:
        """
        Get a variable by ID.
        
        Args:
            variable_id (str): The ID of the variable.
            
        Returns:
            Variable: The variable object.
        """
        response = self.client._send_request(
            'GET',
            f'{self.VARIABLE_ENDPOINT}/{variable_id}'
        )
        return Variable.model_validate(response.json())

    def get_variable_by_name(self, name: str, variable_group_id: str = None) -> Variable:
        """
        Get a variable by name, optionally filtered by variable group ID.
        
        Args:
            name (str): The name of the variable.
            variable_group_id (str, optional): The ID of the variable group to filter by.
            
        Returns:
            Variable: The variable object.
            
        Raises:
            Exception: If the variable is not found.
        """
        variables = self.get_variables(variable_group_id)
        for variable in variables.items:
            if variable.name == name:
                return variable
        raise Exception(f'Could not find variable with name {name}.')

    def create_variable(self, variable: Variable) -> Variable:
        """
        Create a new variable.
        
        Args:
            variable (Variable): The variable to create.
            
        Returns:
            Variable: The created variable object.
        """
        # Handle the case where variable_group_id is provided directly instead of in a reference
        data = variable.model_dump(by_alias=True, exclude_none=True, exclude_defaults=True)
        
        # Ensure restrictions is always included, even if it's the default value
        if 'restrictions' not in data:
            data['restrictions'] = {}
        
        # If both variable_group and variable_group_id are present, use variable_group_id directly
        if 'variableGroupId' in data and 'variableGroup' in data:
            del data['variableGroup']
            
        response = self.client._send_request(
            'POST',
            self.VARIABLE_ENDPOINT,
            data=data
        )
        return Variable.model_validate(response.json())

    def update_variable(self, variable: Variable) -> Variable:
        """
        Update an existing variable.
        
        Args:
            variable (Variable): The variable to update.
            
        Returns:
            Variable: The updated variable object.
        """
        if not variable.variable_type_id:
            raise ValueError("Variable ID is required for update operation")
            
        # Get the data with defaults excluded
        data = variable.model_dump(by_alias=True, exclude_none=True, exclude_defaults=True)
        
        # Ensure restrictions is always included, even if it's the default value
        if 'restrictions' not in data:
            data['restrictions'] = {}
            
        response = self.client._send_request(
            'PUT',
            f'{self.VARIABLE_ENDPOINT}/{variable.variable_type_id}',
            data=data
        )
        return Variable.model_validate(response.json())

    def delete_variable(self, variable_id: str) -> bool:
        """
        Delete a variable.
        
        Args:
            variable_id (str): The ID of the variable to delete.
            
        Returns:
            bool: True if deletion was successful.
            
        Raises:
            Exception: If deletion fails.
        """
        response = self.client._send_request(
            'DELETE',
            f'{self.VARIABLE_ENDPOINT}/{variable_id}'
        )
        if response.status_code != 204:
            raise Exception(f'Failed to delete variable {variable_id}')
        return True
