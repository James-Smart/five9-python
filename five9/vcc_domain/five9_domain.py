from enum import Enum
from ..api.classic_restadmin.restadmin_classic_client import RestAdminClassicAPIClient
from ..models.vcc_domain import Five9VCCDomain

class Region(Enum):
    UK = 'UK'
    EU = 'EU'
    CA = 'CA'
    US = 'US'
    IN = 'IN'

class Five9DomainBuilder:
    '''
    Generates a VCCDomain object from a given domain_id and region.
    '''
    def __init__(self, name: str, region: Region, domain_id: str, username: str, password: str):
        self.region = region
        self.name = name
        self.domain_id = domain_id
        self.base_classic_url = self._get_base_classic_url()
        self.username = username
        self.password = password
        self.classic_client = RestAdminClassicAPIClient(
            self.base_classic_url,
            self.username,
            self.password,
            self.domain_id
            )
        self.object = Five9VCCDomain(
            name = self.name,
            id = self.domain_id,
            prompts = self.classic_client.vcc_prompts.get_all_vccprompts(),
            skills = self.classic_client.common_objects.get_all_skills(),
            inbound_campaigns = self.classic_client.common_objects.get_all_inbound_campaigns(),
            ivr_scripts = self.classic_client.common_objects.get_all_ivr_scripts(),
            contact_fields = self.classic_client.common_objects.get_all_contact_fields(),
            cavs = self.classic_client.common_objects.get_all_cavs(),
            dispositions = self.classic_client.common_objects.get_all_dispositions()

        )

    
    def _get_base_classic_url(self):
        match self.region:
            case Region.UK:
                return 'https://api.five9.eu'
            case Region.EU:
                return 'https://api.eu.five9.com'
            case Region.CA:
                return 'https://api.ca.five9.com'
            case Region.US:
                return 'https://api.five9.com'
            case Region.IN:
                return 'https://api.in.five9.com'
        '''return {
            Region.UK: 'https://api.five9.eu',
            Region.EU: 'https://api.eu.five9.com',
            Region.CA: 'https://api.ca.five9.com',
            Region.US: 'https://api.five9.com',
            Region.IN: 'https://api.in.five9.com'
        }'''