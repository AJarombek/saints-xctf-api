"""
Test suite for the API routes that handle user activation codes (api/src/route/activationCodeRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

from flask import Response
from tests.TestSuite import TestSuite


class TestActivationCodeRoute(TestSuite):

    def test_activation_code_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This route is redirected to
        '/v2/activation_code/' by default.
        """
        response: Response = self.client.post('/v2/activation_code')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/activation_code/', headers.get('Location'))
