"""
Test suite for the main routes describing the API (api/test_src/test_route/apiRoute.py)
Author: Andrew Jarombek
Date: 6/27/2019
"""

import unittest
from flask import Response
from tests.TestSuite import TestSuite


class TestApiRoute(TestSuite):

    def test_entry_route(self) -> None:
        """
        Test the HTTP test_route which is the entry point to the API.
        """
        response: Response = self.client.get('/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self_link'), '/')
        self.assertEqual(response_json.get('api_name'), 'saints-xctf-api')
        self.assertEqual(response_json.get('versions_link'), '/versions')
