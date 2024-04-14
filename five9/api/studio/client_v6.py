from .base_client import BaseAPIClient
from .v6_tasks import StudioV6Tasks
from .v6_prompts import StudioV6Prompts
from .v6_datastores import StudioV6Datatstores


class StudioAPIClientV6(BaseAPIClient):
    """A python interface to the Five9 Studio 6 Datatstore API."""

    def __init__(self, base_url, username, password, api_key, max_requests_per_second=5):
        """Instantiate a new StudioAPIClientV6 object.

        Args:
            base_url (str): The base URL of the Studio instance.
            username (str): The username of the Studio user.
            password (str): The password of the Studio user (taken from the api docs, not login).
            api_key (str): The API key of the Studio user.
            max_requests_per_second (int, optional): The maximum number of requests per second. Defaults to 5.

        """
        super().__init__(base_url, max_requests_per_second)
        self.api_key = api_key
        self.headers = {'Content-Type': 'application/json'}
        self.username = username
        self.password = password
        self._set_token_in_param(
            self._get_token(username, password, api_key))

        self.tasks = StudioV6Tasks(self)
        self.prompts = StudioV6Prompts(self)
        self.datastores = StudioV6Datatstores(self)
