from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator


class DomainReference(BaseModel):
    """Reference to a domain"""
    domain_id: str = Field(alias="domainId")
    uri: str


class VariableRestrictions(BaseModel):
    """Restrictions for a variable"""
    min: Optional[Any] = None
    max: Optional[Any] = None
    regexp: Optional[str] = None
    required: Optional[bool] = False
    predefined_list: Optional[List[str]] = Field(None, alias="predefinedList")
    digits_before: Optional[int] = Field(None, alias="digitsBefore")
    digits_after: Optional[int] = Field(None, alias="digitsAfter")
    date_display_format: Optional[str] = Field(None, alias="dateDisplayFormat")
    time_display_format: Optional[str] = Field(None, alias="timeDisplayFormat")
    time_period_display_format: Optional[str] = Field(None, alias="timePeriodDisplayFormat")
    currency: Optional[str] = None
    default_values: List[Any] = Field(default_factory=list, alias="defaultValues")
    offset_from_current_time: Optional[str] = Field(None, alias="offsetFromCurrentTime")


class VariableReporting(BaseModel):
    """Reporting settings for a variable"""
    apply_to_all_dispositions: Optional[bool] = Field(None, alias="applyToAllDispositions")
    report_when_dispositions: Optional[List[str]] = Field(None, alias="reportWhenDispositions")


class VariableGroupReference(BaseModel):
    """Reference to a variable group"""
    variable_group_id: str = Field(alias="variableGroupId")
    uri: Optional[str] = None


class VariableGroup(BaseModel):
    """
    Represents a variable group in the Five9 system.
    
    Variable groups are containers for variables. Both system and user-defined 
    'custom' variable groups can exist.
    """
    variable_group_id: Optional[str] = Field(None, alias="variableGroupId")
    name: str
    description: Optional[str] = ""
    use_tags: List[str] = Field(default_factory=list, alias="useTags")
    domain: Optional[DomainReference] = None
    uri: Optional[str] = None


class Variable(BaseModel):
    """
    Represents a variable in the Five9 system.
    
    Variables exist within containers called variable groups. Variables have
    a data type, restrictions, and optional reporting settings.
    """
    variable_type_id: Optional[str] = Field(None, alias="variableTypeId")
    name: str
    sensitive: bool = False
    variable_group: Optional[VariableGroupReference] = Field(None, alias="variableGroup")
    variable_group_id: Optional[str] = Field(None, alias="variableGroupId")
    domain: Optional[DomainReference] = None
    use_tags: Optional[List[str]] = Field(None, alias="useTags")
    uri: Optional[str] = None
    description: Optional[str] = None
    data_type: str = Field(alias="dataType")
    reporting: Optional[VariableReporting] = None
    restrictions: VariableRestrictions = Field(default_factory=VariableRestrictions)

    @validator('data_type')
    def validate_data_type(cls, value):
        valid_data_types = {'STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 
                           'TIME', 'TIME_PERIOD', 'PREDEFINED_LIST', 'MONEY'}
        if value not in valid_data_types:
            raise ValueError(f'Invalid data type: {value}')
        return value


class VariableGroupListResponse(BaseModel):
    """Response model for listing variable groups"""
    items: List[VariableGroup] = []


class VariableListResponse(BaseModel):
    """Response model for listing variables"""
    items: List[Variable] = []
