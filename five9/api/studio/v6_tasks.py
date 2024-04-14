from ...models.common import StudioTask


class StudioV6Tasks():
    TASK_LIST_ALL_ENDPOINT = '/studio_instance/studio-api/v1/script/list-all/'

    def __init__(self, client):
        self.client = client

    def get_task_all(self):
        """Returns all tasks for the Studio 6 account.
        """
        response = self.client._send_request(
            'POST',
            self.TASK_LIST_ALL_ENDPOINT
        )
        return [StudioTask.from_dict(d) for d in response.json().get('result', {})]

    def get_task(self, name):
        ''' Given a task name, return its task object, otherwise None'''
        tasks = self.get_task_all()
        for task in tasks:
            if task.name == name:
                return task
        return None
