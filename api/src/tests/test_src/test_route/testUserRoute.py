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

    def test_user_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/' route.  This test proves that the endpoint
        returns a list of users.
        """
        response: Response = self.client.get('/v2/users/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertGreater(len(response_json.get('users')), 1)

        user = response_json.get('users')[0]

        self.assertIn('username', user)
        self.assertIsInstance(user.get('username'), str)
        self.assertIn('first', user)
        self.assertIsInstance(user.get('first'), str)
        self.assertIn('last', user)
        self.assertIsInstance(user.get('last'), str)
        self.assertIn('salt', user)
        self.assertTrue(user.get('salt') is None or type(user.get('salt')) is str)
        self.assertIn('password', user)
        self.assertIsInstance(user.get('password'), str)
        self.assertIn('profilepic', user)
        self.assertTrue(user.get('profilepic') is None or type(user.get('profilepic')) is bytes)
        self.assertIn('profilepic_name', user)
        self.assertTrue(user.get('profilepic_name') is None or type(user.get('profilepic_name')) is str)
        self.assertIn('description', user)
        self.assertTrue(user.get('description') is None or type(user.get('description')) is str)
        self.assertIn('member_since', user)
        self.assertIsInstance(user.get('member_since'), datetime)
        self.assertIn('class_year', user)
        self.assertTrue(user.get('class_year') is None or type(user.get('class_year')) is int)
        self.assertIn('location', user)
        self.assertTrue(user.get('location') is None or type(user.get('location')) is str)
        self.assertIn('favorite_event', user)
        self.assertTrue(user.get('favorite_event') is None or type(user.get('favorite_event')) is str)
        self.assertIn('activation_code', user)
        self.assertIsInstance(user.get('activation_code'), datetime)
        self.assertIn('email', user)
        self.assertTrue(user.get('email') is None or type(user.get('email')) is str)
        self.assertIn('last_signin', user)
        self.assertIsInstance(user.get('last_signin'), datetime)
        self.assertIn('week_start', user)
        self.assertTrue(user.get('week_start') is None or type(user.get('week_start')) is str)
        self.assertIn('subscribed', user)
        self.assertTrue(user.get('subscribed') is None or type(user.get('subscribed')) is str)
        self.assertIn('deleted', user)
        self.assertTrue(user.get('deleted') is None or type(user.get('deleted')) is str)

    def test_user_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users/' route.  This test proves that calling this
        endpoint with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/users/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")
