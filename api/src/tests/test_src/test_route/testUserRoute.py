"""
Test suite for the API routes that handle range view objects (api/src/route/userRoute.py).
Author: Andrew Jarombek
Date: 12/10/2019
"""

import json
from datetime import datetime
from flask import Response
from tests.TestSuite import TestSuite


class TestUserRoute(TestSuite):

    def test_user_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users' route. This route is redirected to
        '/v2/users/' by default.
        """
        response: Response = self.client.get('/v2/users')
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/users/', headers.get('Location'))

    def test_user_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users' route. This route is redirected to
        '/v2/users/' by default.
        """
        response: Response = self.client.post('/v2/users')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/users/', headers.get('Location'))
