from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator, AliasChoices, AliasPath, field_validator
from enum import Enum
import datetime

class User(BaseModel):
    id: str = Field(validation_alias=AliasChoices('userId', 'id'))
    user_name: str = Field(validation_alias=AliasChoices('userName'))
    first_name: Optional[str] = Field(validation_alias=AliasChoices('firstName'), default=None)
    last_name: Optional[str] = Field(validation_alias=AliasChoices('lastName'), default=None)
    full_name: str = Field(validation_alias=AliasChoices('fullName'))
    extension: str = Field(validation_alias=AliasChoices('extension'))
    email: str = Field(validation_alias=AliasChoices('email'))
    can_change_password: bool = Field(validation_alias=AliasChoices('canChangePassword'))
    must_change_password: bool = Field(validation_alias=AliasChoices('mustChangePassword'))
    active: bool = Field(validation_alias=AliasChoices('active'))


class CampaignProfile(BaseModel):
    pass


class CallAttachedVariableType(Enum):
    STRING = 'STRING'
    TIME_PERIOD = 'TIME_PERIOD'
    DATE_TIME = 'DATE_TIME'
    PHONE = 'PHONE'
    EMAIL = 'EMAIL'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    URL = 'URL'


class CallAttachedVariable(BaseModel):
    id: str = Field(validation_alias=AliasChoices('callAttachedVariableId', 'id'))
    group_id: str = Field(validation_alias=AliasChoices('groupId'))
    name: str
    full_name: str = Field(validation_alias=AliasChoices('fullName'), default=None)
    description: Optional[str] = None
    type: CallAttachedVariableType = Field(validation_alias=AliasChoices('type'))
    default_value: Optional[Any] = Field(validation_alias=AliasChoices('defaultValue'), default=None)
    is_reported: bool = Field(validation_alias=AliasChoices('isReported'))
    apply_to_all_dispositions: bool = Field(validation_alias=AliasChoices('applyToAllDispositions'))
    sensitive_data: bool = Field(validation_alias=AliasChoices('sensitiveData'))

class ContactFieldType(Enum):
    SYSTEM = 'SYSTEM'
    CUSTOM = 'CUSTOM'
    MAPPED = 'MAPPED'

class ContactFieldDataType(Enum):
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    DATE_TIME = 'DATE_TIME'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'
    URL = 'URL'

class ContactFieldMappedType(Enum):
    LAST_DISPOSITION = 'LAST_DISPOSITION'
    LAST_AGENT_DISPOSITION_DATE_TIME = 'LAST_AGENT_DISPOSITION_DATE_TIME'
    LAST_AGENT = 'LAST_AGENT'


class ContactFieldDisplayMode(Enum):
    SHORT_LENGTH = 'SHORT_LENGTH'


class ContactField(BaseModel):
    id: str = Field(validation_alias=AliasChoices('contactFieldId', 'id'))
    name: str
    type: ContactFieldType = Field(validation_alias=AliasChoices('contactFieldType', 'type'))
    data_type: ContactFieldDataType = Field(validation_alias=AliasChoices('dataType'))
    mapped_type: Optional[ContactFieldMappedType] = Field(validation_alias=AliasPath('mappedContactField', 'mappedContentType'), default=None)
    date_display_format: Optional[str] = Field(validation_alias=AliasPath('customContactField','restrictions', 'dateDisplayFormat'), default=None)
    time_display_format: Optional[str] = Field(validation_alias=AliasPath('customContactField','restrictions', 'timeDisplayFormat'), default=None)



class Disposition(BaseModel):
    id: str = Field(validation_alias=AliasChoices('dispositionId', 'id'))
    name: str

class Connector(BaseModel):
    id: str = Field(validation_alias=AliasChoices('connectorId', 'id'))
    name: str
    description: Optional[str] = None
    url: Optional[str] = Field(validation_alias=AliasPath('url', 'pathParams', 0, 'value'), default=None)
    method: str = Field(validation_alias=AliasPath('classicConnector', 'method'))

class SkillServiceLevel(BaseModel):
    override_global: bool = Field(validation_alias=AliasChoices('overrideGlobal'))
    speed_of_answer_seconds: Optional[int] = Field(validation_alias=AliasChoices('speedOfAnswerSec'))
    min_time_of_response_seconds: Optional[int] = Field(validation_alias=AliasChoices('minTimeOfResponseSec'))


class Skill(BaseModel):
    id: str = Field(validation_alias=AliasChoices('skillId', 'id'))
    name: str
    description: Optional[str] = None
    #uri: str = Field(validation_alias=AliasChoices('selfUri', 'uri'))
    #has_users: bool = Field(validation_alias=AliasChoices('hasUsers'))
    route_voicemails: bool = Field(validation_alias=AliasChoices('routeVoiceMails'))
    #india_telecom_circle_id: Optional[str] = Field(validation_alias=AliasChoices('indiaTelecomCircleId'))
    #service_level: Optional[SkillServiceLevel] = Field(validation_alias=AliasChoices('serviceLevel'))
    
class IVRScriptBasic(BaseModel):
    id: str = Field(validation_alias=AliasChoices('scriptId', 'id'))
    name: str
    description: Optional[str] = None

class IVRScript(IVRScriptBasic):
    xml: str = Field(validation_alias=AliasChoices('xmlDefinition'))

class CampaignType(Enum):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'
    AUTODIAL = 'AUTODIAL'

class CampaignState(Enum):
    RUNNING = 'RUNNING'
    NOT_RUNNING = 'NOT_RUNNING'


class Campaign(BaseModel):
    id: str = Field(validation_alias=AliasChoices('campaignId', 'id'))
    name: str
    description: Optional[str] = None
    type: CampaignType
    state: CampaignState
    state_since_time: Optional[int] = Field(validation_alias=AliasChoices('stateSinceTime'))

class IVRScheduleDays(Enum):
    SUN = 'SUN'
    MON = 'MON'
    TUE = 'TUE'
    WED = 'WED'
    THU = 'THU'
    FRI = 'FRI'
    SAT = 'SAT'

class IVRScheduleEntryType(Enum):
    SPECIFIC_DATE = 'SPECIFIC_DATE'
    DAYS_OF_WEEK = 'DAYS_OF_WEEK'
    DATE_RANGE = 'DATE_RANGE'

class IVRScriptParameter(BaseModel):
    name: str = Field(validation_alias=AliasPath('name'))
    value: Optional[str] = Field(validation_alias=AliasPath('value', 'value'), default=None)
    type: str = Field(validation_alias=AliasPath('value', 'type'))

class IVRScheduleEntry(BaseModel):
    name: str = Field(validation_alias=AliasPath('generalData','name'))
    script_id: str = Field(validation_alias=AliasPath('generalData', 'script', 'id'))
    script_parameters: Dict[str, IVRScriptParameter] = Field(validation_alias=AliasPath('generalData','scriptParameters'), default={})
    days: Optional[List[IVRScheduleDays]] = Field(validation_alias=AliasPath('generalData','interval', 'days'), default=[])
    date: Optional[datetime.datetime] = Field(validation_alias=AliasPath('generalData','interval', 'date'), default=None)
    all_day: Optional[bool] = Field(validation_alias=AliasPath('generalData','interval', 'allDay'))
    start_time: Optional[datetime.time] = Field(validation_alias=AliasPath('generalData','interval', 'startMinuteOfDay'), default=None)
    end_time: Optional[datetime.time] = Field(validation_alias=AliasPath('generalData','interval', 'untilMinuteOfDay'), default=None)
    start_date: Optional[datetime.datetime] = Field(validation_alias=AliasPath('generalData','interval', 'startDate'), default=None)
    end_date: Optional[datetime.datetime] = Field(validation_alias=AliasPath('generalData','interval', 'untilDate'), default=None)
    voice_channel_enabled: Optional[bool] = Field(validation_alias=AliasPath('voiceChannelEnabled'))

    @field_validator('start_time', 'end_time', mode='before')
    @classmethod
    def convert_time(cls, v: int) -> datetime.time:
        if v is None:
            return None
        else:
            return datetime.time(hour=v // 60, minute=v % 60)
    
    @field_validator('date', 'start_date', 'end_date', mode='before')
    @classmethod
    def convert_date(cls, v: Dict[str, int]) -> datetime.datetime:
        return datetime.datetime(year=v['year'], month=v['month'], day=v['day'])
    
    @field_validator('script_parameters', mode='before')
    @classmethod
    def convert_script_parameters(cls, v: List[IVRScriptParameter]) -> Dict:
        script_parameters = {}
        for script_parameter in v:
            script_parameters[script_parameter['name']] = script_parameter
        return script_parameters
    

class IVRScheduleDefault(BaseModel):
    time_zone: str = Field(validation_alias=AliasPath('timeZoneId'))
    script_id: str = Field(validation_alias=AliasPath('defaultScheduleEntry', 'generalData', 'script', 'id'))
    script_parameters: Dict[str, IVRScriptParameter] = Field(validation_alias=AliasPath('defaultScheduleEntry', 'generalData', 'scriptParameters'), default={})
    
    @field_validator('script_parameters', mode='before')
    @classmethod
    def convert_script_parameters(cls, v: List[IVRScriptParameter]) -> Dict:
        script_parameters = {}
        for script_parameter in v:
            script_parameters[script_parameter['name']] = script_parameter
        return script_parameters



class InboundCampaign(Campaign):
    type: CampaignType = CampaignType.INBOUND
    state: CampaignState = Field(validation_alias=AliasPath('commonCampaignData', 'state'))
    state_since_time: Optional[int] = Field(validation_alias=AliasPath('commonCampaignData', 'stateSinceTime'))
    max_number_of_lines: Optional[int] = Field(validation_alias=AliasPath('maxNumOfLines'))
    max_number_of_vivr_sessions: Optional[int] = Field(validation_alias=AliasPath('maxNumVivrSessions'), default=0)
    nax_number_of_wf_sessions: Optional[int] = Field(validation_alias=AliasPath('maxNumUniversalWfSessions'))
    default_schedule: IVRScheduleDefault = Field(validation_alias=AliasPath('ivrSchedule'), default=None)
    custom_schedules: Optional[List[IVRScheduleEntry]] = Field(validation_alias=AliasPath('ivrSchedule', 'customScheduleEntries'), default=[])
    dnises: Optional[List[str]] = Field(validation_alias=AliasPath('dnises'), default=[])

    @field_validator('dnises', mode='before')
    @classmethod
    def convert_dnises(cls, v) -> List[str]:
        dnis_list = []
        for dnis in v:
            dnis_list.append(dnis['name'])
        return dnis_list




