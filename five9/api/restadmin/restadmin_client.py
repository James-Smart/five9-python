from .base_client import BaseAPIClient
from .context_services import ContextServices
from .vcc_prompts import VCCPrompts
from .speed_dials import SpeedDials

class RestAdminAPIClient(BaseAPIClient):
    def __init__(self, base_url, username, password, domain_id):
        """Instantiate a new RestAdminAPIClient object.

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
        self._set_token_in_param(
            self._get_token(username, password))

        self.context_services = ContextServices(self)
        self.vcc_prompts = VCCPrompts(self)
        self.speed_dials = SpeedDials(self)


