from ...models.five9_prompts import VCCPrompt

class VCCClassicPrompts:
    def __init__(self, client):
        self.client = client
        self.VCCPROMPT_GET_ENDPOINT = f'/restadmin/api/v1/domains/{self.client.domain_id}/prompts'

    def get_all_vccprompts(self):
        response = self.client._send_request(
            'GET',
            self.VCCPROMPT_GET_ENDPOINT,
            )
        prompts = {}
        for item in response.json().get('entities', []):
            prompt = VCCPrompt.model_validate(item)
            prompts[prompt.id] = prompt
        return prompts
    
    def get_full_prompt_by_id(self, id):
        response = self.client._send_request(
            'GET',
            f'{self.VCCPROMPT_GET_ENDPOINT}/{id}',
            )
        return VCCPrompt.model_validate(response.json())