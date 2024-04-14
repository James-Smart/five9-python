from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StudioTask:
    '''Represents a Studio Task object.'''
    id: int
    name: str
    tts_voice_id: int
    configurable: bool
    instance_type: str

    @staticmethod
    def from_dict(d):
        return StudioTask(
            id=int(d['id']),
            name=d['instance_name'],
            tts_voice_id=int(d['tts_voice_id']),
            configurable=True if d['configurable'] == 'yes' else False,
            instance_type=d['instance_type']
        )


@dataclass
class StudioPromptVersion:
    '''An individual prompt, this should belong toa StudioPrompt object'''
    prompt_tts_saml: str
    tts_voice_name: str
    id: Optional[int] = None
    language: Optional[str] = None
    tts_voice_id: Optional[id] = None
    prompt_audio_name: Optional[str] = None
    configurable: Optional[bool] = None

    @staticmethod
    def from_dict(d):
        return StudioPromptVersion(
            id=int(d['id']),
            language=d['language'],
            tts_voice_id=int(d['tts_voice_id']),
            prompt_tts_saml=d['prompt_name_tts'],
            prompt_audio_name=d['prompt_name_audio'],
            tts_voice_name=d['tts_voice_text'],
            configurable=True if d['configurable'] == 'yes' else False
        )


@dataclass
class StudioPrompt:
    '''A collection of StudioPromptVersion objects'''
    id: int
    name: str
    instance_id: int
    versions: List[StudioPromptVersion] = field(default_factory=list)

    @staticmethod
    def from_dict_list(data_list):
        # Assuming all data entries in data_list have the same prompt_id and prompt_name
        prompt_id = int(data_list[0]['prompt_id'])
        prompt_name = data_list[0]['prompt_name']
        instance_id = int(data_list[0]['instance_id'])

        versions = [StudioPromptVersion.from_dict(d) for d in data_list]

        return StudioPrompt(id=prompt_id, name=prompt_name, instance_id=instance_id, versions=versions)
