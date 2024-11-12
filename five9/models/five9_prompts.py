from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator, AliasChoices


class LanguagePrompts(BaseModel):
    name: str = Field(alias='name')
    id: Optional[str] = Field(alias='id')
    self_uri: Optional[str] = Field(alias='selfUri')


class wavPrompt(BaseModel):
    wav_data_base64: str = Field(alias='wavDataBase64')
    wav_data_md5: str = Field(alias='wavDataMd5')


class ttsPrompt(BaseModel):
    builder_xml: str = Field(alias='builderXml')
    ssml: str = Field(alias='ssml')
    wav_data_base64: str = Field(alias='wavDataBase64')
    wav_data_md5: str = Field(alias='wavDataMd5')


class VCCPrompt(BaseModel):
    '''
    Represents a VCC prompt object.
    '''
    name: str = Field(alias='name')
    id: Optional[str] = Field(None, validation_alias=AliasChoices('promptId', 'id'))
    uri: Optional[str] = Field(None, alias='uri')

    description: Optional[str] = Field(valias='description')
    version: Optional[str] = Field(None, alias='version')
    domainLocale: Optional[str] = Field(None, alias='domainLocale')
    # ßtype: str = Field(alias='type')
    is_system: Optional[bool] = Field(None, alias='isSystem')
    is_overridden: Optional[bool] = Field(None, alias='isOverridden')
    duration_millis: Optional[int] = Field(None, alias='durationMillis')
    file_size_bytes: Optional[int] = Field(None, alias='fileSizeBytes')
    kind: Optional[str] = Field(None, alias='kind')
    type: Optional[str] = Field(None, alias='type')
    trace_id: Optional[str] = Field(None, alias='traceId')
    wav_prompt: Optional[wavPrompt] = Field(None, alias='wavPrompt')
    tts_prompt: Optional[ttsPrompt] = Field(None, alias='ttsPrompt')


'''
    @validator('type')
    def validate_data_type(cls, value):
        valid_data_types = {'WAV_PCMU_8K_MONO'}
        if value not in valid_data_types:
            raise ValueError(f'Invalid data type: {value}')
        return value
    '''
