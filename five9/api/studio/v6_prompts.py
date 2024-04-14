from ...models.common import StudioPromptVersion, StudioPrompt
from itertools import groupby


class StudioV6Prompts():
    PROMPT_LIST_ALL_ENDPOINT = '/studio_instance/studio-api/v1/prompt/list-all/'
    PROMPT_LIST_ONE_ENDPOINT = '/studio_instance/studio-api/v1/prompt/list-one/'
    PROMPT_UPDATE_TTS_ENDPOINT = '/studio_instance/studio-api/v1/prompt/update-tts/'

    def __init__(self, client):
        self.client = client

    def get_prompt_all(self, task):
        """Returns all tasks for the Studio 6 account.
        """
        params = {'script_id': str(task.id)}
        print(params)
        response = self.client._send_request(
            'POST',
            self.PROMPT_LIST_ALL_ENDPOINT,
            params=params
        )
        prompt_vers = response.json().get('result', {})
        # prompt_vers = self._build_prompt_ver_list(prompt_vers)
        return self._build_prompt_list(prompt_vers)

    def get_prompt(self, task, id):
        """Returns a prompt given ttaska nd id.
        """
        params = {
            'script_id': task,
            'prompt_id': id
        }
        response = self.client._send_request(
            'POST',
            self.PROMPT_LIST_ONE_ENDPOINT,
            params=params
        )
        return response.json().get('result', {})

    def update_prompt_tts(self, prompt_ver: StudioPromptVersion, task_id: int):
        params = {
            'script_id': str(task_id),
            'prompt_id': str(prompt_ver.id),
            'tts_voice_id': str(prompt_ver.tts_voice_id),
            'prompt_tts': prompt_ver.prompt_tts_saml
        }
        self.client._send_request(
            'POST',
            self.PROMPT_UPDATE_TTS_ENDPOINT,
            params=params
        )
        return True

    def _build_prompt_list(self, prompt_list):
        grouped_prompts = {k: list(v) for k, v in groupby(
            prompt_list, key=lambda x: x['prompt_name'])}
        prompts = [StudioPrompt.from_dict_list(
            grouped_prompts[prompt_name]) for prompt_name in grouped_prompts]
        return prompts

    def _build_prompt_ver_list(self, prompt_ver_list):
        ret = []
        for prompt in prompt_ver_list:
            ret.append(StudioPromptVersion.from_dict(prompt))
        return ret
