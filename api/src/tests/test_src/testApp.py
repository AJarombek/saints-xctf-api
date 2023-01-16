"""
Test suite for the entrypoint to the Flask application (api/test_src/app.py)
Author: Andrew Jarombek
Date: 6/22/2019
"""

from flask import current_app, Response
from tests.TestSuite import TestSuite


class TestApp(TestSuite):
    def test_app_exists(self):
        """
        Test asserting that the current app import is truthy as expected.
        """
        self.assertTrue(current_app is not None)

    def test_non_existent_route(self) -> None:
        """
        Test performing an HTTP GET request against an endpoint that doesn't exist. This query should invoke the
        custom 404 error handler.
        """
        response: Response = self.client.get("/path/doesnt/exist")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json.get("error_description"), "Page Not Found")
        self.assertGreater(len(response_json.get("exception")), 0)
        self.assertEqual(response_json.get("contact"), "andrew@jarombek.com")
        self.assertEqual(response_json.get("api_index"), "/versions")
