# Five9 Python API Client

A Python library for interacting with Five9 CCaaS (Contact Center as a Service) APIs.

## Overview

This library provides an easy way to interact with various Five9 APIs, including:
- REST Admin API
- Studio API V6, V7
- Context Services API
- Call Attached Variables (CAVs)

## Installation

```bash
pip install five9-python
```
It's recommended to target a particular version of the library to avoid breaking changes in the future. You can specify a version in your `requirements.txt` file:

```plaintext
five9-python==VERSION_NUMBER
```

## Available Clients

### RestAdminAPIClient

Client for interacting with the Five9 REST Admin API.

```python
from five9 import RestAdminAPIClient

client = RestAdminAPIClient(
    base_url='https://api.five9.com',
    username='your-username',
    password='your-password',
    domain_id='your-domain-id'
)

# Example: Get CAV variable groups
groups = client.cav.get_variable_groups()
```

### RestAdminClassicAPIClient

Client for interacting with the Five9 Classic REST Admin API.

```python
from five9 import RestAdminClassicAPIClient

client = RestAdminClassicAPIClient(
    base_url='https://api.five9.com',
    username='your-username',
    password='your-password',
    domain_id='your-domain-id'
)

# Example: Get VCC prompts
prompt = client.vcc_prompts.get_full_prompt_by_id('prompt-id')
```

### StudioAPIClientV6

Client for interacting with the Five9 Studio API V6.

```python
from five9 import StudioAPIClientV6, Filter

client = StudioAPIClientV6(
    base_url='https://ukstudio.inferencecommunications.com',
    username='your-username',
    password='your-password',
    api_key='your-api-key'
)

# Example: Get datastore row by ID
row = client.datastore.get_datastore_row_byid(datastore_id='100', row_id='123')

# Example: Search datastore with filters
filter_id = Filter(column_name="id")
filter_id.equals("123")
rows = client.datastore.get_datastore_search_rows(datastore_id='100', filters=[filter_id])
```

## Utilities

### VCCDomainBuilder

An in progress utility for pulling most objects from a VCC domain - with a plan to allow running IVR test cases.

```python
from five9 import VCCDomainBuilder, Region

domain = VCCDomainBuilder(
    name="Domain Name",
    region=Region.UK,
    domain_id="your-domain-id",
    username="your-username",
    password="your-password"
)
```

### Filter

Utility for creating filters for API queries.

```python
from five9 import Filter

# Create a filter for timestamp less than or equal to a specific date
filter_timestamp = Filter(column_name="timestamp")
filter_timestamp.less_than_or_equal_to("2024-07-26 15:30:00")

# Create a filter for exact ID match
filter_id = Filter(column_name="id")
filter_id.equals("123")
```

## Context Services API

The Five9 Context Services API allows you to work with data tables, attributes, rows, and queries.

```python
from five9 import RestAdminAPIClient
from five9.models.context_services_model import Datatable, Attribute, Row

client = RestAdminAPIClient(
    base_url='https://api.five9.com',
    username='your-username',
    password='your-password',
    domain_id='your-domain-id'
)

# Create a new data table
datatable = Datatable(
    dataTableName="Customer_Info",
    dataTableDescription="Customer information table"
)
created_datatable = client.context_services.add_datatable(datatable)

# Get a data table by name
datatable = client.context_services.get_datatable_by_name("Customer_Info")

# Add an attribute (column) to the data table
attribute = Attribute(
    dataTableId=datatable.id,
    attributeName="customer_id",
    dataType="STRING"
)
client.context_services.add_attribute(attribute)

# Add another attribute
phone_attr = Attribute(
    dataTableId=datatable.id,
    attributeName="phone_number",
    dataType="STRING"
)
client.context_services.add_attribute(phone_attr)

# Get all attributes for a data table
datatable = client.context_services.get_attibutes(datatable)

# Add a new row to the data table
row_data = {
    "customer_id": "12345",
    "phone_number": "+1234567890"
}
client.context_services.add_new_row(datatable, row_data)

# Create a query
query_id = client.context_services.create_query(
    datatable.id,
    "Find_Customer",
    "Query to find customer by ID"
)

# Create a composite filter
filter_id = client.context_services.create_composite_filter(
    datatable.id,
    query_id,
    "AND"
)

# Add a property filter to the composite filter
attribute = datatable.get_attribute_by_name("customer_id")
client.context_services.create_property_filter(
    datatable.id,
    query_id,
    filter_id,
    attribute.id,
    attribute.name,
    "EQUAL"
)
```

## Working with Call Attached Variables (CAVs)

Call Attached Variables (CAVs) are used to store and manage data associated with calls within the Five9 platform. They are organized into variable groups and can be used in various Five9 components like IVR scripts, campaigns, and agent desktop applications.

```python
from five9 import RestAdminAPIClient
from five9.models.cav import Variable, VariableGroup

# Initialize the client
client = RestAdminAPIClient(
    base_url='https://api.five9.com',
    username='your-username',
    password='your-password',
    domain_id='your-domain-id'
)

# Get all variable groups
variable_groups = client.cav.get_variable_groups()
print(f"Found {len(variable_groups.items)} variable groups")

# Create a new variable group
new_group = VariableGroup(
    name="Customer Data",
    description="Variables for storing customer information"
)
created_group = client.cav.create_variable_group(new_group)
print(f"Created variable group with ID: {created_group.variable_group_id}")

# Create a new variable in the group
new_variable = Variable(
    name="customer_id",
    description="Unique customer identifier",
    data_type="STRING",
    variable_group_id=created_group.variable_group_id,
    restrictions={
        "required": True,
        "regexp": "^[A-Z]{2}\\d{6}$"  # Format: 2 uppercase letters followed by 6 digits
    }
)
created_variable = client.cav.create_variable(new_variable)
print(f"Created variable with ID: {created_variable.variable_type_id}")

# Find and update a specific variable
# First, find the variable group by name
target_group_name = "Customer Data"
target_group = None

for group in variable_groups.items:
    if group.name == target_group_name:
        target_group = group
        break

if target_group:
    # Get all variables in the group
    variables = client.cav.get_variables(variable_group_id=target_group.variable_group_id)
    
    # Find a specific variable by name
    target_variable_name = "customer_id"
    target_variable = None
    
    for var in variables.items:
        if var.name == target_variable_name:
            target_variable = var
            break
    
    if target_variable:
        # Update the variable
        target_variable.description = "Updated customer identifier"
        updated_variable = client.cav.update_variable(target_variable)
        print(f"Updated variable: {updated_variable.name}")
```

### Working with Variable Restrictions

CAVs support various data types and restrictions:

```python
# String variable with regex validation
string_var = Variable(
    name="email",
    data_type="STRING",
    variable_group_id=group_id,
    restrictions={
        "regexp": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    }
)

# Numeric variable with min/max constraints
numeric_var = Variable(
    name="age",
    data_type="INTEGER",
    variable_group_id=group_id,
    restrictions={
        "min": 18,
        "max": 120
    }
)

# Predefined list variable
list_var = Variable(
    name="status",
    data_type="PREDEFINED_LIST",
    variable_group_id=group_id,
    restrictions={
        "predefined_list": ["New", "Active", "Suspended", "Closed"]
    }
)

# Date variable
date_var = Variable(
    name="birth_date",
    data_type="DATE",
    variable_group_id=group_id,
    restrictions={
        "date_display_format": "MM/dd/yyyy"
    }
)
```

## Features

- Easy-to-use Python interface for Five9 APIs
- Support for multiple Five9 API types
- Helper utilities for common operations
- Typed models for API responses

## License

See the [LICENSE](LICENSE) file for details.
