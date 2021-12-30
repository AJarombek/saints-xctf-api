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
        response: Response = self.client.post('/v2/activation_code', headers={'Authorization': f'Bearer {self.jwt}'})
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
        response: Response = self.client.post('/v2/activation_code/', headers={'Authorization': f'Bearer {self.jwt}'})
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
            headers={'Authorization': f'Bearer {self.jwt}'}
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
            headers={'Authorization': f'Bearer {self.jwt}'}
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
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})

        # Create a new code (this should succeed)
        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), True)

        activation_code_json = response_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))
        self.assertEqual(1, activation_code_json.get('group_id'))
        self.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
        self.assertIn('expiration_date', activation_code_json)

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
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(post_response.status_code, 200)

        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))

        response: Response = self.client.get(
            f'/v2/activation_code/exists/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), f'/v2/activation_code/exists/{activation_code}')
        self.assertEqual(response_json.get('matching_code_exists'), True)

    def test_activation_code_exists_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/exists/<code>' route.  This test proves that
        if the code exists in the database a 400 failure response will be returned.
        """
        # Ensure that the code doesn't exist by hard deleting it.
        self.client.delete('/v2/activation_code/60UN03', headers={'Authorization': f'Bearer {self.jwt}'})

        response: Response = self.client.get(
            '/v2/activation_code/exists/60UN03',
            headers={'Authorization': f'Bearer {self.jwt}'}
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
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(post_response.status_code, 200)

        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))

        response: Response = self.client.get(f'/v2/activation_code/{activation_code}', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), f'/v2/activation_code/{activation_code}')

        activation_code_json = response_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))
        self.assertEqual(1, activation_code_json.get('group_id'))
        self.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
        self.assertIn('expiration_date', activation_code_json)

    def test_activation_code_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/<code>' route.  This test proves that if the
        activation code searched for doesn't exist, the endpoint returns a 400 HTTP error status.
        """

        # Ensure that the code doesn't exist by hard deleting it.
        self.client.delete('/v2/activation_code/60UN03', headers={'Authorization': f'Bearer {self.jwt}'})

        response: Response = self.client.get('/v2/activation_code/60UN03', headers={'Authorization': f'Bearer {self.jwt}'})
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

    def test_activation_code_delete_route_400_other_users_code(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/<code>' route.  This test proves that the
        endpoint should return a 400 error status if the activation code exists, but it belongs to another user.
        """
        request_body = json.dumps({'email': 'saintsxctf@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(post_response.status_code, 200)

        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        response: Response = self.client.delete(
            f'/v2/activation_code/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), f'/v2/activation_code/{activation_code}')
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual(
            response_json.get('error'),
            f'User andy is not authorized to delete activation code {activation_code}.'
        )

    def test_activation_code_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/<code>' route.  This test proves that the
        endpoint should return a 400 failure status if the activation code does not exist.
        """
        response: Response = self.client.delete(
            f'/v2/activation_code/TESTCD',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual(response_json.get('error'), 'there is no existing activation code with this code')

    def test_activation_code_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/<code>' route.  This test proves that the
        endpoint should return a 204 success status if the activation code exists.
        """
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(post_response.status_code, 200)

        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        response: Response = self.client.delete(
            f'/v2/activation_code/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
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
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        self.assertEqual(post_response.status_code, 200)
        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        response: Response = self.client.delete(
            f'/v2/activation_code/soft/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

    def test_activation_code_soft_delete_route_400_does_not_exist(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that if
        the activation code the user is trying to soft delete doesn't exist, a 400 error code is returned.
        """

        # Ensure that the activation code was already deleted before testing the DELETE endpoint.
        self.client.delete('/v2/activation_code/TESTCD', headers={'Authorization': f'Bearer {self.jwt}'})

        response: Response = self.client.delete(
            '/v2/activation_code/soft/TESTCD',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/soft/TESTCD')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'there is no existing activation code with this code')

    def test_activation_code_soft_delete_route_400_other_users_code(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that
        the endpoint should return a 400 error status if the activation code exists, but it belongs to another user.
        """
        request_body = json.dumps({'email': 'saintsxctf@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(post_response.status_code, 200)

        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        response: Response = self.client.delete(
            f'/v2/activation_code/soft/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), f'/v2/activation_code/soft/{activation_code}')
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual(
            response_json.get('error'),
            f'User andy is not authorized to soft delete activation code {activation_code}.'
        )

    def test_activation_code_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/activation_code/soft/<code>' route.  This test proves that
        if the activation code was already soft deleted, the endpoint returns a 400 error code.
        """
        # Ensure that the activation code exists before testing the DELETE endpoint
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
        post_response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        self.assertEqual(post_response.status_code, 200)
        response_json: dict = post_response.get_json()
        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        response: Response = self.client.delete(
            f'/v2/activation_code/soft/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.delete(
            f'/v2/activation_code/soft/{activation_code}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), f'/v2/activation_code/soft/{activation_code}')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'there is no existing activation code with this code')

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
