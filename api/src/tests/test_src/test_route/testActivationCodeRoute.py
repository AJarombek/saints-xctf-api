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
        Test performing an HTTP POST request on the '/v2/activation_code' route. This test proves that a request body
        with a proper activation code should succeed if the activation code does not already exist.
        """
        # First hard delete the existing code if it exists
        self.client.delete('/v2/activation_code/60UN02')

        request_body = json.dumps({'activation_code': '60UN02'})

        # Then attempt to create a new code (this should succeed)
        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json'
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
        self.client.delete('/v2/activation_code/AJAJAJ')

        # The first request to create an activation code will succeed.
        request_body = json.dumps({'activation_code': 'AJAJAJ'})

        response: Response = self.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json'
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
            content_type='application/json'
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/activation_code')
        self.assertEqual(response_json.get('added'), False)
        self.assertEqual(response_json.get('activation_code'), None)
        self.assertEqual(response_json.get('error'), 'failed to create a new activation code')

    def test_activation_code_exists_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/exists/<code>' route.  This test proves that
        if the code exists in the database a 200 success response will be returned.
        """
        # Ensure that the activation code exists prior to testing for existence.
        self.client.delete('/v2/activation_code/60UN02')
        request_body = json.dumps({'activation_code': '60UN02'})
        post_response = self.client.post('/v2/activation_code/', data=request_body, content_type='application/json')
        self.assertEqual(post_response.status_code, 200)

        response: Response = self.client.get('/v2/activation_code/exists/60UN02')
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
        self.client.delete('/v2/activation_code/60UN03')

        response: Response = self.client.get('/v2/activation_code/exists/60UN03')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/exists/60UN03')
        self.assertEqual(response_json.get('matching_code_exists'), False)

    def test_activation_code_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/activation_code/<code>' route.  This test proves that if the
        activation code searched for exists, a 200 status code and a JSON object with the code is returned
        """

        # Ensure that the activation code exists prior to retrieval.
        self.client.delete('/v2/activation_code/60UN02')
        request_body = json.dumps({'activation_code': '60UN02'})
        post_response = self.client.post('/v2/activation_code/', data=request_body, content_type='application/json')
        self.assertEqual(post_response.status_code, 200)

        response: Response = self.client.get('/v2/activation_code/60UN02')
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
        self.client.delete('/v2/activation_code/60UN03')

        response: Response = self.client.get('/v2/activation_code/60UN03')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/60UN03')
        self.assertEqual(response_json.get('activation_code'), None)
        self.assertEqual(response_json.get('error'), 'there is no matching activation code')

    def test_activation_code_delete_route_204(self) -> None:
        # Ensure that the activation code exists before testing the DELETE endpoint
        request_body = json.dumps({'activation_code': 'TESTCD'})
        self.client.post('/v2/activation_code/', data=request_body, content_type='application/json')

        response: Response = self.client.delete('/v2/activation_code/TESTCD')
        self.assertEqual(response.status_code, 204)

    def test_activation_code_soft_delete_route_204(self) -> None:
        # Ensure that the activation code exists before testing the DELETE endpoint
        self.client.delete('/v2/activation_code/TESTCD')

        request_body = json.dumps({'activation_code': 'TESTCD'})
        self.client.post('/v2/activation_code/', data=request_body, content_type='application/json')

        response: Response = self.client.delete('/v2/activation_code/soft/TESTCD')
        self.assertEqual(response.status_code, 204)

    def test_activation_code_soft_delete_route_400_does_not_exist(self) -> None:
        # Ensure that the activation code was already deleted before testing the DELETE endpoint.
        self.client.delete('/v2/activation_code/TESTCD')

        response: Response = self.client.delete('/v2/activation_code/soft/TESTCD')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/soft/TESTCD')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'there is no existing activation code with this code')

    def test_activation_code_soft_delete_route_400_already_deleted(self) -> None:
        # Ensure that the activation code was already soft deleted before testing the DELETE endpoint
        self.client.delete('/v2/activation_code/TESTCD')
        request_body = json.dumps({'activation_code': 'TESTCD'})
        self.client.post('/v2/activation_code/', data=request_body, content_type='application/json')
        self.client.delete('/v2/activation_code/soft/TESTCD')

        response: Response = self.client.delete('/v2/activation_code/soft/TESTCD')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/soft/TESTCD')
        self.assertEqual(response_json.get('deleted'), False)
        self.assertEqual(response_json.get('error'), 'this activation code is already soft deleted')

    def test_activation_code_get_links_route_200(self) -> None:
        response: Response = self.client.get('/v2/activation_code/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/activation_code/links')
        self.assertEqual(len(response_json.get('endpoints')), 4)
