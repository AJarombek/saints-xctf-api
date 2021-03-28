"""
Test suite for the API routes that handle a user's flair (api/src/route/flairRoute.py)
Author: Andrew Jarombek
Date: 10/26/2019
"""

import json

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestFlairRoute(TestSuite):

    def test_flair_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/flair' route. This route is redirected to
        '/v2/flair/' by default.
        """
        response: Response = self.client.post('/v2/flair', headers={'Authorization': f'Bearer {self.jwt}'})
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/flair/', headers.get('Location'))

    def test_flair_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/flair' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/flair', AuthVariant.FORBIDDEN)

    def test_flair_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/flair' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/flair', AuthVariant.UNAUTHORIZED)

    def test_flair_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/flair/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/flair/', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/flair')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('flair'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_flair_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/flair/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        request_body = json.dumps({"username": "andy"})

        response: Response = self.client.post(
            '/v2/flair/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/flair')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('flair'))
        self.assertEqual(
            response_json.get('error'),
            "'username' and 'flair' are required fields"
        )

    def test_flair_post_route_400_other_user(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/flair/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 400 error code if a user is trying to create a flair for
        another user.
        """
        request_body = json.dumps({
            "username": "andy2",
            "flair": "Website Creator"
        })

        response: Response = self.client.post(
            '/v2/flair/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/flair')
        self.assertFalse(response_json.get('added'))
        self.assertIsNone(response_json.get('flair'))
        self.assertEqual(
            response_json.get('error'),
            "User andy is not authorized to create a flair for user andy2."
        )

    def test_flair_post_route_201(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/flair/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 201 success code and a new flair object.
        """
        request_body = json.dumps({
            "username": "andy",
            "flair": "Website Creator"
        })

        response: Response = self.client.post(
            '/v2/flair/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/flair')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('flair'))

    def test_flair_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/flair/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/flair/', AuthVariant.FORBIDDEN)

    def test_flair_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/flair/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/flair/', AuthVariant.UNAUTHORIZED)

    def test_flair_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/flair/links' route.  This test proves that calling
        this endpoint returns a list of other flair endpoints.
        """
        response: Response = self.client.get('/v2/flair/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/flair/links')
        self.assertEqual(len(response_json.get('endpoints')), 1)
