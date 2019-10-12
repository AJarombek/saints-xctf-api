"""
Test suite for the API routes that handle user activation codes (api/src/route/activationCodeRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

import json
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

    def test_activation_code_post_route_400(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code/' route. This test proves that an empty
        request body will result in a 400 status code response.
        """
        response: Response = self.client.post('/v2/activation_code/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_activation_code_post_route_400_empty_request(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that an empty
        JSON in the request body will result in a 400 status code response.
        """
        request_body = json.dumps({})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json'
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('error'), "'activation_code' is a required field")

    def test_activation_code_post_route_400_invalid_code(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that a request body
        with an activation code of the incorrect length results in a 400 status code response.
        """
        request_body = json.dumps({'activation_code': 'invalid'})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json'
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('error'), "'activation_code' must be a string of length 6")

    def test_activation_code_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves ...
        """
        request_body = json.dumps({'activation_code': '60UN02'})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json'
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
