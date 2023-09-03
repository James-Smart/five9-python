import pytest
from unittest.mock import Mock
from five9.api.v6_datastores import StudioV6Datatstores

# Mock the client's _send_request method


@pytest.fixture
def mocked_client():
    client = Mock()
    return client


@pytest.fixture
def datastore_instance(mocked_client):
    return StudioV6Datatstores(mocked_client)


def test_get_datastore_id(datastore_instance, mocked_client):
    mocked_client._send_request.return_value.json.return_value = {
        'result': [{'name': 'test_datastore', 'id': '1234'}]
    }

    result = datastore_instance.get_datastore_id('test_datastore')
    assert result == '1234'

    with pytest.raises(Exception) as e:
        datastore_instance.get_datastore_id('not_found')
    assert str(e.value) == 'Could not find datastore with name not_found.'


def test_get_datastore_row_byid(datastore_instance, mocked_client):
    mocked_client._send_request.return_value.json.return_value = {
        'result': {'id': '1234', 'name': 'test_row'}
    }

    result = datastore_instance.get_datastore_row_byid('ds_id', '1234')
    assert result == {'id': '1234', 'name': 'test_row'}


def test_get_datastore_audio_file(datastore_instance, mocked_client):
    mocked_client._send_request.return_value.content = b'audio_content'

    result = datastore_instance.get_datastore_audio_file(
        'ds_id', '1234', 'audio_column')
    assert result == b'audio_content'


def test_get_datastore_search_rows(datastore_instance, mocked_client):
    mocked_client._send_request.return_value.json.return_value = {
        'result': [{'id': '1234', 'name': 'test_row'}]
    }

    result = datastore_instance.get_datastore_search_rows('ds_id')
    assert result == [{'id': '1234', 'name': 'test_row'}]
