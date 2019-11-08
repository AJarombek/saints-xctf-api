"""
Test suite for the API routes that handle forgot password codes assigned to a user
(api/src/route/forgotPasswordRoute.py)
Author: Andrew Jarombek
Date: 11/5/2019
"""

import json
from flask import Response
from tests.TestSuite import TestSuite


class TestForgotPasswordRoute(TestSuite):

    def test_forgot_password_get_route_200_empty(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/<username>' route.  This test proves that
        trying to retrieve a forgot password code for a user that doesn't exist results in a successful HTTP 200 error
        with an empty list returned.
        """
        response: Response = self.client.get('/v2/forgot_password/fake_user')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/fake_user')
        self.assertEqual(response_json.get('forgot_password_codes'), [])

    def test_forgot_password_get_route_200_populated(self) -> None:
        # Ensure that at least one forgot password code exists for this user
        self.client.post('/v2/forgot_password/andy')

        response: Response = self.client.get('/v2/forgot_password/andy')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/andy')
        self.assertGreaterEqual(len(response_json.get('forgot_password_codes')), 1)

    def test_forgot_password_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/links' route.  This test proves that calling
        this endpoint returns a list of other forgot password endpoints.
        """
        response: Response = self.client.get('/v2/forgot_password/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/links')
        self.assertEqual(len(response_json.get('endpoints')), 2)
