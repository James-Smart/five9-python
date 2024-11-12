from ...models.vcc_general import *
from devtools import pprint

class CommonObjects:
    def __init__(self, client):
        self.client = client
        self.SKILL_GET_ENDPOINT = f'/restadmin/api/v1/domains/{self.client.domain_id}/skills'

    def get_all_skills(self):
        response = self.client._send_request(
            'GET',
            self.SKILL_GET_ENDPOINT,
        )
        skills = {}
        print(response.json())
        for item in response.json().get('entities', []):
            skill = Skill.model_validate(item)
            skills[skill.id] = skill
        return skills
    
    def get_all_ivr_scripts(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/scripts/',
        )
        scripts = {}
        for item in response.json().get('entities', []):
            script = IVRScriptBasic.model_validate(item)
            scripts[script.id] = script
        return scripts
    
    def get_ivr_script_by_id(self, id):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/scripts/{id}',
        )
        return IVRScript.model_validate(response.json())
    
    def get_all_campaigns(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/campaigns/',
        )
        campaigns = []
        for item in response.json().get('entities', []):
            campaign = Campaign.model_validate(item)
            campaigns.append(campaign)
        
        return campaigns
    
    def get_all_inbound_campaigns(self):
        campaigns = self.get_all_campaigns()
        inbound_campaigns = {}
        for campaign in campaigns:
            if campaign.type == CampaignType.INBOUND:
                inbound_campaigns[campaign.id] = (self.get_inbound_campaign_by_id(campaign.id))
        return inbound_campaigns
    
    def get_campaign_by_id(self, id):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/campaigns/{id}',
        )
        pprint(response.json())
        return response.json()
    
    def get_inbound_campaign_by_id(self, id):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/campaigns/inbound_campaigns/{id}',
        )

        return InboundCampaign.model_validate(response.json())
        #return response.json()
    
    def get_all_contact_fields(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/contact-fields/',
        )
        contact_fields = {}
        for item in response.json().get('entities', []):
            contact_field = ContactField.model_validate(item)
            contact_fields[contact_field.id] = contact_field
        return contact_fields
    
    def get_all_cavs(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/call-variables/',
        )
        cavs = {}
        for item in response.json().get('entities', []):
            cav = CallAttachedVariable.model_validate(item)
            cavs[cav.id] = cav
        return cavs
    
    def get_all_dispositions(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/dispositions/',
        )
        dispositions = {}
        for item in response.json().get('entities', []):
            disposition = Disposition.model_validate(item)
            dispositions[disposition.id] = disposition
        return dispositions
    
    def get_all_connectors(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/connectors/',
        )
        connectors = {}
        for item in response.json().get('entities', []):
            connector = Connector.model_validate(item)
            connectors[connector.id] = connector
        return connectors
    
    def get_all_users(self):
        response = self.client._send_request(
            'GET',
            f'/restadmin/api/v1/domains/{self.client.domain_id}/users/',
        )
        users = {}
        for item in response.json().get('entities', []):
            user = User.model_validate(item)
            users[user.id] = user
        return users

