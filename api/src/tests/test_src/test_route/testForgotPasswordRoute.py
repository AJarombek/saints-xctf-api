"""
Test suite for the API routes that handle forgot password codes assigned to a user
(api/src/route/forgotPasswordRoute.py)
Author: Andrew Jarombek
Date: 11/5/2019
"""

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestForgotPasswordRoute(TestSuite):

    def test_forgot_password_get_route_400_empty(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/<username>' route.  This test proves that
        trying to retrieve a forgot password code for a user that doesn't exist results in a HTTP 400 error code
        with an empty list returned.
        """
        response: Response = self.client.get('/v2/forgot_password/fake_user', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/fake_user')
        self.assertEqual(response_json.get('forgot_password_codes'), [])

    def test_forgot_password_get_route_200_populated(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/<username>' route.  This test proves that
        trying to retrieve a forgot password code for a valid user with existing forgot password codes results in one
        or more forgot password codes and a successful HTTP 200 code.
        """
        # Ensure that at least one forgot password code exists for this user
        self.client.post('/v2/forgot_password/andy', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.get('/v2/forgot_password/andy', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/andy')
        self.assertGreaterEqual(len(response_json.get('forgot_password_codes')), 1)

    def test_forgot_password_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/forgot_password/andy', AuthVariant.FORBIDDEN)

    def test_forgot_password_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/forgot_password/andy', AuthVariant.UNAUTHORIZED)

    def test_forgot_password_post_route_400(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/forgot_password/<username>' route.  This test proves that
        calling this endpoint with a invalid username results in a 400 error code.
        """
        response: Response = self.client.post(
            '/v2/forgot_password/fake_user',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/fake_user')
        self.assertFalse(response_json.get('inserted'))
        self.assertEquals(response_json.get('error'), 'There is no user associated with this username/email.')

    def test_forgot_password_post_route_201(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/forgot_password/<username>' route.  This test proves that
        calling this endpoint with a valid username results in a new forgot password code being created.
        """
        response: Response = self.client.post('/v2/forgot_password/andy', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/forgot_password/andy')
        self.assertTrue(response_json.get('inserted'))
        self.assertIsNotNone(response_json.get('forgot_password_code'))

    def test_forgot_password_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/forgot_password/andy', AuthVariant.FORBIDDEN)

    def test_forgot_password_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/forgot_password/andy', AuthVariant.UNAUTHORIZED)

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
