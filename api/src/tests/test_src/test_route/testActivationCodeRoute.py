"""
Test suite for the API routes that handle user activation codes (api/src/route/activationCodeRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

import json
from flask import Response
import unittest

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestActivationCodeRoute(TestSuite):

    def test_activation_code_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This route is redirected to
        '/v2/activation_code/' by default.
        """
        response: Response = self.client.post('/v2/activation_code', headers={'Authorization': 'Bearer j.w.t'})
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/activation_code/', headers.get('Location'))

    def test_activation_code_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/activation_code' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/activation_code', AuthVariant.FORBIDDEN)

    def test_activation_code_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/activation_code' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/activation_code', AuthVariant.UNAUTHORIZED)

    def test_activation_code_post_route_400(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code/' route. This test proves that an empty
        request body will result in a 400 status code response.
        """
        response: Response = self.client.post('/v2/activation_code/', headers={'Authorization': 'Bearer j.w.t'})
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
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('error'), "'group_id' and 'email' are required fields")

    def test_activation_code_post_route_400_missing_fields(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that a request body
        with missing email or group_id fields results in a 400 status code response.
        """
        request_body = json.dumps({'activation_code': 'invalid'})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('error'), "'group_id' and 'email' are required fields")

    def test_activation_code_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that a request body
        with a proper activation code should succeed if the activation code does not already exist.
        """
        # First hard delete the existing code if it exists
        self.client.delete('/v2/activation_code/60UN02', headers={'Authorization': 'Bearer j.w.t'})

        request_body = json.dumps({'activation_code': '60UN02'})

        # Then attempt to create a new code (this should succeed)
        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), True)
        self.assertEqual(response_json.get('activation_code'), {'activation_code': '60UN02', 'deleted': None})

    def test_activation_code_post_route_500_already_exists(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that a request body
        with a proper activation code should FAIL with a 500 error if the activation code already exists.
        """
        self.client.delete('/v2/activation_code/AJAJAJ', headers={'Authorization': 'Bearer j.w.t'})

        # The first request to create an activation code will succeed.
        request_body = json.dumps({'activation_code': 'AJAJAJ'})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), True)
        self.assertEqual(response_json.get('activation_code'), {'activation_code': 'AJAJAJ', 'deleted': None})

        # The second request to create an activation code will fail.
        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('activation_code'), None)
        self.assertEqual(response_json.get('error'), 'failed to create a new activation code')

    def test_activation_code_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/activation_code/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/activation_code/', AuthVariant.FORBIDDEN)

    def test_activation_code_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/activation_code/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/activation_code/', AuthVariant.UNAUTHORIZED)

    def test_activation_code_exists_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/exists/<code>' route.  This test proves that
        if the code exists in the database a 200 success response will be returned.
        """
        # Ensure that the activation code exists prior to testing for existence.
        self.client.delete('/v2/activation_code/60UN02', headers={'Authorization': 'Bearer j.w.t'})
        request_body = json.dumps({'activation_code': '60UN02'})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(post_response.status_code, 200)

        response: Response = self.client.get(
            '/v2/activation_code/exists/60UN02',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/exists/60UN02')
        self.assertEqual(response_json.get('matching_code_exists'), True)

    def test_activation_code_exists_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/exists/<code>' route.  This test proves that
        if the code exists in the database a 400 failure response will be returned.
        """
        # Ensure that the code doesn't exist by hard deleting it.
        self.client.delete('/v2/activation_code/60UN03', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.get(
            '/v2/activation_code/exists/60UN03',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/exists/60UN03')
        self.assertEqual(response_json.get('matching_code_exists'), False)

    def test_activation_code_exists_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/activation_code/exists/<code>' route.
        You are a great person.
        """
        test_route_auth(self, self.client, 'GET', '/v2/activation_code/exists/60UN02', AuthVariant.FORBIDDEN)

    def test_activation_code_exists_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/activation_code/exists/<code>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/activation_code/exists/60UN02', AuthVariant.UNAUTHORIZED)

    def test_activation_code_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/<code>' route.  This test proves that if the
        activation code searched for exists, a 200 status code and a JSON object with the code is returned
        """

        # Ensure that the activation code exists prior to retrieval.
        self.client.delete('/v2/activation_code/60UN02', headers={'Authorization': 'Bearer j.w.t'})
        request_body = json.dumps({'activation_code': '60UN02'})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(post_response.status_code, 200)

        response: Response = self.client.get('/v2/activation_code/60UN02', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/60UN02')
        self.assertEqual(response_json.get('activation_code'), {'activation_code': '60UN02', 'deleted': None})

    def test_activation_code_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/<code>' route.  This test proves that if the
        activation code searched for doesn't exist, the endpoint returns a 400 HTTP error status.
        """

        # Ensure that the code doesn't exist by hard deleting it.
        self.client.delete('/v2/activation_code/60UN03', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.get('/v2/activation_code/60UN03', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/60UN03')
        self.assertEqual(response_json.get('activation_code'), None)
        self.assertEqual(response_json.get('error'), 'there is no matching activation code')

    def test_activation_code_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/activation_code/<code>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/activation_code/60UN02', AuthVariant.FORBIDDEN)

    def test_activation_code_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/activation_code/<code>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/activation_code/60UN02', AuthVariant.UNAUTHORIZED)

    def test_activation_code_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/<code>' route.  This test proves that the
        endpoint should return a 204 success status, no matter if the code existed or not.
        """

        response: Response = self.client.delete('/v2/activation_code/TESTCD', headers={'Authorization': 'Bearer j.w.t'})
        self.assertEqual(response.status_code, 204)

    def test_activation_code_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/activation_code/<code>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/activation_code/TESTCD', AuthVariant.FORBIDDEN)

    def test_activation_code_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/activation_code/<code>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/activation_code/TESTCD', AuthVariant.UNAUTHORIZED)

    def test_activation_code_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that if
        the activation code exists and wasn't already soft deleted, the endpoint will return a successful 204 status.
        """

        # Ensure that the activation code exists before testing the DELETE endpoint
        self.client.delete('/v2/activation_code/TESTCD', headers={'Authorization': 'Bearer j.w.t'})

        request_body = json.dumps({'activation_code': 'TESTCD'})
        self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response: Response = self.client.delete(
            '/v2/activation_code/soft/TESTCD',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(response.status_code, 204)

    def test_activation_code_soft_delete_route_400_does_not_exist(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that if
        the activation code the user is trying to soft delete doesn't exist, a 400 error code is returned.
        """

        # Ensure that the activation code was already deleted before testing the DELETE endpoint.
        self.client.delete('/v2/activation_code/TESTCD', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.delete(
            '/v2/activation_code/soft/TESTCD',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/soft/TESTCD')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'there is no existing activation code with this code')

    @unittest.skip('There activation code is no longer supplied by the user, instead dynaically created by the server.')
    def test_activation_code_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that
        if the activation code was already soft deleted, the endpoint returns a 400 error code.
        """

        # Ensure that the activation code was already soft deleted before testing the DELETE endpoint
        self.client.delete('/v2/activation_code/TESTCD', headers={'Authorization': 'Bearer j.w.t'})
        request_body = json.dumps({'activation_code': 'TESTCD'})
        self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.client.delete('/v2/activation_code/soft/TESTCD', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.delete(
            '/v2/activation_code/soft/TESTCD',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/soft/TESTCD')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'this activation code is already soft deleted')

    def test_activation_code_soft_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/activation_code/soft/TESTCD', AuthVariant.FORBIDDEN)

    def test_activation_code_soft_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/activation_code/soft/TESTCD', AuthVariant.UNAUTHORIZED)

    def test_activation_code_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/links' route.  This test proves that calling
        this endpoint returns a list of other activation code endpoints.
        """
        response: Response = self.client.get('/v2/activation_code/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/links')
        self.assertEqual(len(response_json.get('endpoints')), 4)
