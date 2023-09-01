#!/usr/bin/env python

"""Tests for `five9_studio` package."""

import pytest
from unittest.mock import patch, Mock

from five9_studio.api import client_v6


def test_get_token():
    with patch('five9_studio.api.client_v6.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"token": "dummy_token"}}
        mock_post.return_value = mock_response

        client = client_v6.StudioAPIClientV6(
            'https://ukstudio.inferencecommunications.com', "username", "password", "api_key")
        token = client._get_token("username", "password", "api_key")

        assert token == "dummy_token"


def test_get_datastore_id():
    # Patching both client_v6's and base_client's post methods
    with patch('five9_studio.api.client_v6.requests.post') as mock_client_post, \
            patch('five9_studio.api.base_client.requests.post') as mock_base_post:

        # Mock response for client_v6's _get_token
        mock_client_response = Mock()
        mock_client_response.status_code = 200
        mock_client_response.json.return_value = {
            "result": {"token": "dummy_token"}}
        mock_client_post.return_value = mock_client_response

        # Mock response for base_client's request to get datastore IDs
        mock_base_response = Mock()
        mock_base_response.status_code = 200
        mock_base_response.json.return_value = {
            "result": [
                {"name": "test_datastore", "id": 21},
                {"name": "another_datastore", "id": 45}
            ]
        }
        mock_base_post.return_value = mock_base_response

        client = client_v6.StudioAPIClientV6(
            "http://testurl.com", "username", "password", "api_key")
        datastore_id = client.get_datastore_id("test_datastore")

        assert datastore_id == 21
