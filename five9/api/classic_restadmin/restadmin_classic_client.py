from ..restadmin.base_client import BaseAPIClient
from .vcc_prompts_classic import VCCClassicPrompts
from .common_objects import CommonObjects

class RestAdminClassicAPIClient(BaseAPIClient):
    def __init__(self, base_url, username, password, domain_id):
        """Instantiate a new RestAdminClassicAPIClient object.

        Args:
            base_url (str): The base URL of the VCC instance.
            username (str): The username of the VCC admin user.
            password (str): The password of the VCC admin user.
            max_requests_per_second (int, optional): The maximum number of requests per second. Defaults to 5.

        """
        super().__init__(base_url)
        self.base_url = base_url
        self.username = username
        self.password = password
        self.domain_id = domain_id
        self._set_basic_auth()

        self.vcc_prompts = VCCClassicPrompts(self)
        self.common_objects = CommonObjects(self)



