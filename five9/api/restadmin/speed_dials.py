from ...models.speed_dials import SpeedDial
from typing import List


class SpeedDials:

    def __init__(self, client):
        self.client = client
        self.SPEEDDIALS_ENDPOINT = f'/users/v1/domains/{self.client.domain_id}/speed-dials'

    def add_speed_dial(self, speed_dial: SpeedDial) -> SpeedDial:
        '''
        Given a SpeedDial model, creates a new speed dial
        '''
        response = self.client._send_request(
            'POST',
            self.SPEEDDIALS_ENDPOINT,
            data=speed_dial.model_dump(
                by_alias=True, exclude_none=True, exclude_defaults=True)
        )
        return SpeedDial.model_validate(response.json())

    def get_all_speed_dials(self) -> List[SpeedDial]:
        """Get all speed dials with pagination support.

        Returns:
            List[SpeedDial]: A list of all speed dials.
        """
        speed_dials = []
        next_page = self.SPEEDDIALS_ENDPOINT

        while next_page:
            response = self.client._send_request(
                'GET',
                next_page
            )
            data = response.json()
            speed_dials.extend([SpeedDial.model_validate(item) for item in data.get('items', [])])
            next_page = data.get('paging', {}).get('next')

        return speed_dials
   
