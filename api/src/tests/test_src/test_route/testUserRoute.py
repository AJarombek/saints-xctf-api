"""
Test suite for the API routes that handle range view objects (api/src/route/userRoute.py).
Author: Andrew Jarombek
Date: 12/10/2019
"""

import json
from datetime import datetime
import unittest
import asyncio

import aiohttp
from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestUserRoute(TestSuite):

    def test_user_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users' route. This route is redirected to
        '/v2/users/' by default.
        """
        response: Response = self.client.get(
            '/v2/users',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/users/', headers.get('Location'))

    def test_user_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users', AuthVariant.FORBIDDEN)

    def test_user_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users', AuthVariant.UNAUTHORIZED)

    def test_user_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users' route. This route is redirected to
        '/v2/users/' by default.
        """
        response: Response = self.client.post(
            '/v2/users',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/users/', headers.get('Location'))

    @unittest.skip('User Creation Does Not Require JWT Authorization')
    def test_user_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/users' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users', AuthVariant.FORBIDDEN)

    @unittest.skip('User Creation Does Not Require JWT Authorization')
    def test_user_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/users' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users', AuthVariant.UNAUTHORIZED)

    def test_user_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/' route.  This test proves that the endpoint
        returns a list of users.
        """
        response: Response = self.client.get(
            '/v2/users/',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
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
        self.assertNotIn('profilepic', user)
        self.assertIn('profilepic_name', user)
        self.assertTrue(user.get('profilepic_name') is None or type(user.get('profilepic_name')) is str)
        self.assertIn('description', user)
        self.assertTrue(user.get('description') is None or type(user.get('description')) is str)
        self.assertIn('member_since', user)
        self.assertIsInstance(user.get('member_since'), str)
        self.assertIn('class_year', user)
        self.assertTrue(user.get('class_year') is None or type(user.get('class_year')) is int)
        self.assertIn('location', user)
        self.assertTrue(user.get('location') is None or type(user.get('location')) is str)
        self.assertIn('favorite_event', user)
        self.assertTrue(user.get('favorite_event') is None or type(user.get('favorite_event')) is str)
        self.assertIn('activation_code', user)
        self.assertIsInstance(user.get('activation_code'), str)
        self.assertIn('email', user)
        self.assertTrue(user.get('email') is None or type(user.get('email')) is str)
        self.assertIn('last_signin', user)
        self.assertIsInstance(user.get('last_signin'), str)
        self.assertIn('week_start', user)
        self.assertTrue(user.get('week_start') is None or type(user.get('week_start')) is str)
        self.assertIn('subscribed', user)
        self.assertTrue(user.get('subscribed') is None or type(user.get('subscribed')) is str)
        self.assertIn('deleted', user)
        self.assertIsInstance(user.get('deleted'), bool)

    def test_user_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/', AuthVariant.FORBIDDEN)

    def test_user_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/', AuthVariant.UNAUTHORIZED)

    def test_user_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users/' route.  This test proves that calling this
        endpoint with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post(
            '/v2/users/',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), "The request body isn't populated.")

    def test_user_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users/' route.  This test proves that calling this
        endpoint with missing required fields results in a 400 error.
        """
        # Missing the required 'password' field
        request_body = json.dumps({
            "username": "andy",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "member_since": "2019-12-12",
            "activation_code": "ABC123",
            "last_signin": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(
            response_json.get('error'),
            "'username', 'first', 'last', 'email', 'password', and 'activation_code' are required fields"
        )

    def test_user_post_route_400_invalid_activation_code(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users/' route.  This test proves that calling
        this endpoint with a valid user object but an invalid activation code results in a 400 error.
        """
        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy1',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        request_body = json.dumps({
            "username": "andy1",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "B0unD2",
            "description": "It doesn't matter how you tell them, the fact you told them is what will be "
                           "beautiful and perfect to them.",
            "member_since": "2019-12-12",
            "activation_code": "ABC123",
            "last_signin": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), "The activation code is invalid or expired.")

    def test_user_post_route_201(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/users/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new user object.
        """
        # Before trying to create the user, make sure that the activation code already exists.
        request_body = json.dumps({'group_id': 1, 'email': 'andrew@jarombek.com'})
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
        activation_code = activation_code_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))
        self.assertEqual(1, activation_code_json.get('group_id'))
        self.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
        self.assertIn('expiration_date', activation_code_json)

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy2',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        request_body = json.dumps({
            "username": "andy2",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "B0unD2",
            "description": "If it's me, you know that just saying hi to me makes me happy.  Please don't be hard on "
                           "yourself if you can't or aren't ready yet.  It's okay, I'm still always here for you.",
            "member_since": str(datetime.fromisoformat('2019-12-13')),
            "activation_code": activation_code,
            "last_signin": str(datetime.fromisoformat('2019-12-14'))
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(
            201,
            response.status_code,
            msg=f"Unexpected status code.  Response: {response_json.get('error')}"
        )
        self.assertEqual(response_json.get('self'), '/v2/users')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('user'))

        user = response_json.get('user')
        self.assertIn('username', user)
        self.assertIn('first', user)
        self.assertIn('last', user)
        self.assertIn('salt', user)
        self.assertIn('password', user)
        self.assertNotIn('profilepic', user)
        self.assertIn('profilepic_name', user)
        self.assertIn('description', user)
        self.assertIn('member_since', user)
        self.assertIn('class_year', user)
        self.assertIn('location', user)
        self.assertIn('favorite_event', user)
        self.assertIn('activation_code', user)
        self.assertIn('email', user)
        self.assertIn('last_signin', user)
        self.assertIn('week_start', user)
        self.assertIn('subscribed', user)
        self.assertIn('deleted', user)

    @unittest.skip('User Creation Does Not Require JWT Authorization')
    def test_user_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/users/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users/', AuthVariant.FORBIDDEN)

    @unittest.skip('User Creation Does Not Require JWT Authorization')
    def test_user_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/users/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users/', AuthVariant.UNAUTHORIZED)

    def test_user_by_username_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/<username>' route.  This test proves
        that trying to retrieve a user with a username that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            '/v2/users/invalid_username',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/invalid_username')
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'there is no user with this username')

    def test_user_by_username_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/<username>' route.  This test proves that
        retrieving a user with a valid username results in the user and a 200 status.
        """
        response: Response = self.client.get(
            '/v2/users/andy',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy')
        self.assertIsNotNone(response_json.get('user'))

    def test_user_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/andy', AuthVariant.FORBIDDEN)

    def test_user_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/andy', AuthVariant.UNAUTHORIZED)

    def test_user_by_username_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>' route.  This test proves that
        trying to update a user that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put(
            '/v2/users/invalid_username',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/invalid_username')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'there is no existing user with this username')

    def test_user_by_username_put_route_400_updating_other_user(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>' route.  This test proves that
        trying to update a user which is different than the one authenticated results in a 400 error.
        """
        response: Response = self.client.put(
            '/v2/users/andy2',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'User andy is not authorized to update user andy2.')

    def test_user_by_username_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>' route.  This test proves that
        if the updated user is the same as the original user, a 400 error is returned.
        """
        response: Response = self.client.get(
            '/v2/users/andy',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('user'))

        request_body = json.dumps(response_json.get('user'))

        response: Response = self.client.put(
            '/v2/users/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/andy')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(
            response_json.get('error'),
            'the user submitted is equal to the existing user with the same username'
        )

    def test_user_by_username_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>' route.  This test proves that
        if a valid user JSON is passed to this endpoint, the existing user will be updated and a valid
        200 response code will be returned.
        """
        request_body = json.dumps({
            "username": "andy",
            "first": "Andy",
            "last": "Jarombek",
            "email": "andrew@jarombek.com",
            "profilepic": None,
            "profilepic_name": None,
            "description": "I sometimes like to run.",
            "class_year": "2017",
            "location": "Riverside, CT",
            "favorite_event": "5000m, 8K",
            "week_start": "monday",
        })

        response: Response = self.client.put(
            '/v2/users/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy')
        self.assertTrue(response_json.get('updated'))
        self.assertIsNotNone(response_json.get('user'))

        # Confirm the fields were updated as expected.
        self.assertNotIn('profilepic', response_json.get('user'))
        self.assertIn('profilepic_name', response_json.get('user'))
        self.assertIn('favorite_event', response_json.get('user'))
        self.assertEqual(response_json.get('user').get('favorite_event'), '5000m, 8K')
        self.assertIn('email', response_json.get('user'))
        self.assertEqual(response_json.get('user').get('email'), 'andrew@jarombek.com')

    def test_user_by_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy', AuthVariant.FORBIDDEN)

    def test_user_by_username_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy', AuthVariant.UNAUTHORIZED)

    def test_user_by_username_delete_route_403(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/<username>' route.  This test proves
        that the endpoint is disabled even with proper validation.
        """
        response: Response = self.client.delete('/v2/users/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        self.assertEqual(response.status_code, 403)

    def test_user_by_username_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/users/andy', AuthVariant.FORBIDDEN)

    def test_user_by_username_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/users/<username>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/users/andy', AuthVariant.UNAUTHORIZED)

    def test_user_by_username_soft_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/soft/<username>' route.  This test
        proves that if the user doesn't exist, a 400 error is returned.
        """
        # Ensure that the user was already deleted before testing the DELETE endpoint
        self.client.delete(
            '/v2/users/invalid_user',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        response: Response = self.client.delete(
            '/v2/users/soft/invalid_user',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))

    def test_user_by_username_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/soft/<username>' route.  This test
        proves that if the user was already soft deleted, a 400 error is returned.
        """
        # Before trying to create the user, make sure that the activation code already exists.
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
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
        activation_code = activation_code_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))
        self.assertEqual(1, activation_code_json.get('group_id'))
        self.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
        self.assertIn('expiration_date', activation_code_json)

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy3',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        request_body = json.dumps({
            "username": "andy3",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "password",
            "activation_code": activation_code
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        username = response_json.get('user').get('username')

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_user_by_username_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/soft/<username>' route.  This test proves that
        soft deleting an existing non-soft deleted user will execute successfully and return a valid 204 status.
        """
        # Before trying to create the user, make sure that the activation code already exists.
        request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})

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
        activation_code = activation_code_json.get('activation_code')
        self.assertEqual(6, len(activation_code_json.get('activation_code')))
        self.assertEqual(1, activation_code_json.get('group_id'))
        self.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
        self.assertIn('expiration_date', activation_code_json)

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy3',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        request_body = json.dumps({
            "username": "andy3",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "password",
            "activation_code": activation_code
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201, msg=f'Error creating user: {response_json.get("error")}')
        username = response_json.get('user').get('username')

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

    def test_user_by_username_soft_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/users/soft/<username>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/users/soft/andy3', AuthVariant.FORBIDDEN)

    def test_user_by_username_soft_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/users/soft/<username>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/users/soft/andy3', AuthVariant.UNAUTHORIZED)

    def test_user_snapshot_by_username_get_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/snapshot/<username>' route.  This test proves that
        trying to get a snapshot about a user that doesn't exist results in a 400 error.
        """
        # A very important song, but not a username used on the website.
        response: Response = self.client.get(
            '/v2/users/snapshot/bound2',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/snapshot/bound2')
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'there is no user with this username')

    def test_user_snapshot_by_username_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/snapshot/<username>' route.  This test proves that
        trying to get a snapshot about a user is successful if the user exists.
        """
        # A very important song, but not a username used on the website.
        response: Response = self.client.get(
            '/v2/users/snapshot/andy',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/snapshot/andy')
        self.assertIsNotNone(response_json.get('user'))

        user = response_json.get('user')

        # The snapshot should have all the traditional user fields...
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
        self.assertNotIn('profilepic', user)
        self.assertIn('profilepic_name', user)
        self.assertTrue(user.get('profilepic_name') is None or type(user.get('profilepic_name')) is str)
        self.assertIn('description', user)
        self.assertTrue(user.get('description') is None or type(user.get('description')) is str)
        self.assertIn('member_since', user)
        self.assertIsInstance(user.get('member_since'), str)
        self.assertIn('class_year', user)
        self.assertTrue(user.get('class_year') is None or type(user.get('class_year')) is int)
        self.assertIn('location', user)
        self.assertTrue(user.get('location') is None or type(user.get('location')) is str)
        self.assertIn('favorite_event', user)
        self.assertTrue(user.get('favorite_event') is None or type(user.get('favorite_event')) is str)
        self.assertIn('activation_code', user)
        self.assertIsInstance(user.get('activation_code'), str)
        self.assertIn('email', user)
        self.assertTrue(user.get('email') is None or type(user.get('email')) is str)
        self.assertIn('last_signin', user)
        self.assertIsInstance(user.get('last_signin'), str)
        self.assertIn('week_start', user)
        self.assertTrue(user.get('week_start') is None or type(user.get('week_start')) is str)
        self.assertIn('subscribed', user)
        self.assertTrue(user.get('subscribed') is None or type(user.get('subscribed')) is str)
        self.assertIn('deleted', user)
        self.assertIsInstance(user.get('deleted'), bool)

        # ... along with additional fields
        self.assertIn('flair', user)
        self.assertIsInstance(user.get('flair'), list)
        self.assertIn('forgotpassword', user)
        self.assertIsInstance(user.get('forgotpassword'), list)
        self.assertIn('groups', user)
        self.assertIsInstance(user.get('groups'), list)
        self.assertIn('notifications', user)
        self.assertIsInstance(user.get('notifications'), list)
        self.assertIn('statistics', user)
        self.assertIsInstance(user.get('statistics'), dict)

        # I just finished knitting a blanket for my Mom.  I knitted one for Lisa's wedding as well.  If I'm lucky
        # one day I'll get to ask you if you want one as well.
        statistics = user.get('statistics')
        self.assertIn('miles_all_time', statistics)
        self.assertTrue(statistics.get('miles_all_time') is None or type(statistics.get('miles_all_time')) is float)
        self.assertIn('miles_past_month', statistics)
        self.assertTrue(statistics.get('miles_past_month') is None or type(statistics.get('miles_past_month')) is float)
        self.assertIn('miles_past_week', statistics)
        self.assertTrue(statistics.get('miles_past_week') is None or type(statistics.get('miles_past_week')) is float)
        self.assertIn('miles_past_year', statistics)
        self.assertTrue(statistics.get('miles_past_year') is None or type(statistics.get('miles_past_year')) is float)
        self.assertIn('run_miles_all_time', statistics)
        self.assertTrue(statistics.get('run_miles_all_time') is None or type(statistics.get('run_miles_all_time')) is float)
        self.assertIn('run_miles_past_year', statistics)
        self.assertTrue(statistics.get('run_miles_past_year') is None or type(statistics.get('run_miles_past_year')) is float)
        self.assertIn('run_miles_past_month', statistics)
        self.assertTrue(statistics.get('run_miles_past_month') is None or type(statistics.get('run_miles_past_month')) is float)
        self.assertIn('run_miles_past_week', statistics)
        self.assertTrue(statistics.get('run_miles_past_week') is None or type(statistics.get('run_miles_past_week')) is float)
        self.assertIn('feel_all_time', statistics)
        self.assertTrue(statistics.get('feel_all_time') is None or type(statistics.get('feel_all_time')) is float)
        self.assertIn('feel_past_year', statistics)
        self.assertTrue(statistics.get('feel_past_year') is None or type(statistics.get('feel_past_year')) is float)
        self.assertIn('feel_past_month', statistics)
        self.assertTrue(statistics.get('feel_past_month') is None or type(statistics.get('feel_past_month')) is float)
        self.assertIn('feel_past_week', statistics)
        self.assertTrue(statistics.get('feel_past_week') is None or type(statistics.get('feel_past_week')) is float)

    def test_user_snapshot_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/snapshot/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/snapshot/andy', AuthVariant.FORBIDDEN)

    def test_user_snapshot_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/snapshot/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/snapshot/andy', AuthVariant.UNAUTHORIZED)

    def test_user_groups_by_username_get_route_200(self) -> None:
        """
        Test performing a successful HTTP GET request on the '/v2/users/groups/<username>' route.
        """
        response: Response = self.client.get('/v2/users/groups/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/groups/andy')

        groups = response_json.get('groups')
        self.assertGreater(len(groups), 0)

        group = groups[0]
        self.assertIn('group_name', group)
        self.assertTrue(group.get('group_name') is None or type(group.get('group_name')) is str)
        self.assertIn('group_title', group)
        self.assertTrue(group.get('group_title') is None or type(group.get('group_title')) is str)
        self.assertIn('status', group)
        self.assertTrue(group.get('status') is None or type(group.get('status')) is str)
        self.assertIn('user', group)
        self.assertTrue(group.get('user') is None or type(group.get('user')) is str)

    def test_user_groups_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/groups/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/groups/andy', AuthVariant.FORBIDDEN)

    def test_user_groups_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/groups/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/groups/andy', AuthVariant.UNAUTHORIZED)

    def test_user_teams_by_username_get_route_200(self) -> None:
        """
        Test performing a successful HTTP GET request on the '/v2/users/teams/<username>' route.
        """
        response: Response = self.client.get('/v2/users/teams/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/teams/andy')

        teams = response_json.get('teams')
        self.assertGreater(len(teams), 0)

        team = teams[0]
        self.assertIn('team_name', team)
        self.assertTrue(team.get('team_name') is None or type(team.get('team_name')) is str)
        self.assertIn('title', team)
        self.assertTrue(team.get('title') is None or type(team.get('title')) is str)
        self.assertIn('status', team)
        self.assertTrue(team.get('status') is None or type(team.get('status')) is str)
        self.assertIn('user', team)
        self.assertTrue(team.get('user') is None or type(team.get('user')) is str)

    def test_user_teams_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/teams/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/teams/andy', AuthVariant.FORBIDDEN)

    def test_user_teams_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/teams/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/teams/andy', AuthVariant.UNAUTHORIZED)

    def test_user_memberships_by_username_get_route_200(self) -> None:
        """
        Test performing a successful HTTP GET request on the '/v2/users/memberships/<username>' route.
        """
        response: Response = self.client.get('/v2/users/memberships/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')

        memberships = response_json.get('memberships')
        self.assertGreater(len(memberships), 0)

        team_membership = memberships[0]
        self.assertIn('team_name', team_membership)
        self.assertTrue(team_membership.get('team_name') is None or type(team_membership.get('team_name')) is str)
        self.assertIn('title', team_membership)
        self.assertTrue(team_membership.get('title') is None or type(team_membership.get('title')) is str)
        self.assertIn('status', team_membership)
        self.assertTrue(team_membership.get('status') is None or type(team_membership.get('status')) is str)
        self.assertIn('user', team_membership)
        self.assertTrue(team_membership.get('user') is None or type(team_membership.get('user')) is str)
        self.assertIn('groups', team_membership)
        self.assertTrue(team_membership.get('groups') is None or type(team_membership.get('groups')) is list)

        groups = team_membership.get('groups')
        self.assertGreaterEqual(len(groups), 0)

        if len(groups) > 0:
            group_membership = groups[0]
            self.assertIn('group_name', group_membership)
            self.assertTrue(group_membership.get('group_name') is None or type(group_membership.get('group_name')) is str)
            self.assertIn('group_title', group_membership)
            self.assertTrue(group_membership.get('group_title') is None or type(group_membership.get('group_title')) is str)
            self.assertIn('status', group_membership)
            self.assertTrue(group_membership.get('status') is None or type(group_membership.get('status')) is str)
            self.assertIn('user', group_membership)
            self.assertTrue(group_membership.get('user') is None or type(group_membership.get('user')) is str)

    def test_user_memberships_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/memberships/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/memberships/andy', AuthVariant.FORBIDDEN)

    def test_user_memberships_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/memberships/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/memberships/andy', AuthVariant.UNAUTHORIZED)

    def test_user_memberships_by_username_put_route_leave_join_groups_201(self) -> None:
        """
        Test performing a successful HTTP PUT request on the '/v2/users/memberships/<username>' route by leaving and
        joining groups.
        """
        request_body = json.dumps({
            'teams_joined': [],
            'teams_left': [],
            'groups_joined': [{'team_name': 'saintsxctf', 'group_name': 'mensxc'}],
            'groups_left': [{'team_name': 'saintsxctf', 'group_name': 'alumni'}]
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertTrue(response_json.get('updated'))

        request_body = json.dumps({
            'teams_joined': [],
            'teams_left': [],
            'groups_joined': [{'team_name': 'saintsxctf', 'group_name': 'alumni'}],
            'groups_left': [{'team_name': 'saintsxctf', 'group_name': 'mensxc'}]
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertTrue(response_json.get('updated'))

    def test_user_memberships_by_username_put_route_leave_join_teams_201(self) -> None:
        """
        Test performing a successful HTTP PUT request on the '/v2/users/memberships/<username>' route by leaving and
        joining teams.
        """
        request_body = json.dumps({
            'teams_joined': ['saintsxctf_alumni'],
            'teams_left': ['saintsxctf'],
            'groups_joined': [],
            'groups_left': []
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertTrue(response_json.get('updated'))

        request_body = json.dumps({
            'teams_joined': ['saintsxctf'],
            'teams_left': ['xc_alumni'],
            'groups_joined': [{'team_name': 'saintsxctf', 'group_name': 'alumni'}],
            'groups_left': []
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertTrue(response_json.get('updated'))

    def test_user_memberships_by_username_put_route_500_invalid_team(self) -> None:
        """
        Test performing an unsuccessful HTTP PUT request on the '/v2/users/memberships/<username>' route by joining a
        team that doesnt exist.
        """
        request_body = json.dumps({
            'teams_joined': ['invalid'],
            'teams_left': [],
            'groups_joined': [],
            'groups_left': []
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertFalse(response_json.get('updated'))
        self.assertEqual(response_json.get('error'), "failed to update the user's memberships")

    def test_user_memberships_by_username_put_route_500_invalid_group(self) -> None:
        """
        Test performing an unsuccessful HTTP PUT request on the '/v2/users/memberships/<username>' route by joining a
        group that doesnt exist.
        """
        request_body = json.dumps({
            'teams_joined': [],
            'teams_left': [],
            'groups_joined': [{'team_name': 'saintsxctf', 'group_name': 'invalid'}],
            'groups_left': []
        })

        response: Response = self.client.put(
            '/v2/users/memberships/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/memberships/andy')
        self.assertFalse(response_json.get('updated'))
        self.assertEqual(response_json.get('error'), "failed to update the user's memberships")

    def test_user_memberships_by_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/users/memberships/<username>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/memberships/andy', AuthVariant.FORBIDDEN)

    def test_user_memberships_by_username_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/users/memberships/<username>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/memberships/andy', AuthVariant.UNAUTHORIZED)

    def test_user_notifications_by_username_get_route_200(self) -> None:
        """
        Test performing a successful HTTP GET request on the '/v2/users/notifications/<username>' route.
        """
        response: Response = self.client.get('/v2/users/notifications/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/notifications/andy')

        notifications = response_json.get('notifications')
        self.assertGreater(len(notifications), 0)

        notification = notifications[0]
        self.assertIn('notification_id', notification)
        self.assertTrue(notification.get('notification_id') is None or type(notification.get('notification_id')) is int)
        self.assertIn('username', notification)
        self.assertTrue(notification.get('username') is None or type(notification.get('username')) is str)
        self.assertIn('time', notification)
        self.assertTrue(notification.get('time') is None or type(notification.get('time')) is str)
        self.assertIn('link', notification)
        self.assertTrue(notification.get('link') is None or type(notification.get('link')) is str)
        self.assertIn('viewed', notification)
        self.assertTrue(notification.get('viewed') is None or type(notification.get('viewed')) is str)
        self.assertIn('description', notification)
        self.assertTrue(notification.get('description') is None or type(notification.get('description')) is str)

    def test_user_notifications_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/notifications/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/notifications/andy', AuthVariant.FORBIDDEN)

    def test_user_notifications_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/notifications/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/notifications/andy', AuthVariant.UNAUTHORIZED)

    def test_user_flair_by_username_get_route_200(self) -> None:
        """
        Test performing a successful HTTP GET request on the '/v2/users/flair/<username>' route.
        """
        response: Response = self.client.get('/v2/users/flair/andy', headers={'Authorization': f'Bearer {self.jwt}'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/flair/andy')

        flair_list = response_json.get('flair')
        self.assertGreater(len(flair_list), 0)

        flair = flair_list[0]
        self.assertIn('flair_id', flair)
        self.assertTrue(flair.get('flair_id') is None or type(flair.get('flair_id')) is int)
        self.assertIn('username', flair)
        self.assertTrue(flair.get('username') is None or type(flair.get('username')) is str)
        self.assertIn('flair', flair)
        self.assertTrue(flair.get('flair') is None or type(flair.get('flair')) is str)

    def test_user_flair_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/flair/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/flair/andy', AuthVariant.FORBIDDEN)

    def test_user_flair_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/flair/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/flair/andy', AuthVariant.UNAUTHORIZED)

    def test_user_statistics_by_username_get_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/statistics/<username>' route.  This test proves that
        trying to get statistics for a user that doesn't exist results in a 400 error.
        """
        # So. Much. Salad.
        response: Response = self.client.get(
            '/v2/users/statistics/bound2',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/statistics/bound2')
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'there is no user with this username')

    def test_user_statistics_by_username_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/statistics/<username>' route.  This test proves that
        trying to get a user's statistics is successful if the user exists.
        """
        response: Response = self.client.get(
            '/v2/users/statistics/andy',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/statistics/andy')
        self.assertIsNotNone(response_json.get('stats'))

        statistics = response_json.get('stats')

        self.assertIn('miles_all_time', statistics)
        self.assertTrue(statistics.get('miles_all_time') is None or type(statistics.get('miles_all_time')) is float)
        self.assertIn('miles_past_month', statistics)
        self.assertTrue(statistics.get('miles_past_month') is None or type(statistics.get('miles_past_month')) is float)
        self.assertIn('miles_past_week', statistics)
        self.assertTrue(statistics.get('miles_past_week') is None or type(statistics.get('miles_past_week')) is float)
        self.assertIn('miles_past_year', statistics)
        self.assertTrue(statistics.get('miles_past_year') is None or type(statistics.get('miles_past_year')) is float)
        self.assertIn('run_miles_all_time', statistics)
        self.assertTrue(statistics.get('run_miles_all_time') is None or type(statistics.get('run_miles_all_time')) is float)
        self.assertIn('run_miles_past_year', statistics)
        self.assertTrue(statistics.get('run_miles_past_year') is None or type(statistics.get('run_miles_past_year')) is float)
        self.assertIn('run_miles_past_month', statistics)
        self.assertTrue(statistics.get('run_miles_past_month') is None or type(statistics.get('run_miles_past_month')) is float)
        self.assertIn('run_miles_past_week', statistics)
        self.assertTrue(statistics.get('run_miles_past_week') is None or type(statistics.get('run_miles_past_week')) is float)
        self.assertIn('feel_all_time', statistics)
        self.assertTrue(statistics.get('feel_all_time') is None or type(statistics.get('feel_all_time')) is float)
        self.assertIn('feel_past_year', statistics)
        self.assertTrue(statistics.get('feel_past_year') is None or type(statistics.get('feel_past_year')) is float)
        self.assertIn('feel_past_month', statistics)
        self.assertTrue(statistics.get('feel_past_month') is None or type(statistics.get('feel_past_month')) is float)
        self.assertIn('feel_past_week', statistics)
        self.assertTrue(statistics.get('feel_past_week') is None or type(statistics.get('feel_past_week')) is float)

    def test_user_statistics_by_username_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/users/statistics/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/statistics/andy', AuthVariant.FORBIDDEN)

    def test_user_statistics_by_username_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/users/statistics/<username>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/users/statistics/andy', AuthVariant.UNAUTHORIZED)

    def test_user_change_password_by_username_put_route_500_missing_required_field(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with missing required fields results in a 500 error.
        """
        # Missing the required 'new_password' field
        request_body = json.dumps({
            "forgot_password_code": "123456"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), False)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), False)
        self.assertEqual(
            response_json.get('error'),
            "'forgot_password_code' and 'new_password' are required fields."
        )

    def test_user_change_password_by_username_put_route_500_invalid_code(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with an invalid forgot password results in a 500 status code.
        """
        request_body = json.dumps({
            "forgot_password_code": "123456",
            "new_password": "abcd1234"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), False)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), False)
        self.assertEqual(
            response_json.get('error'),
            "This forgot password code is invalid."
        )

    def test_user_change_password_by_username_put_route_500_other_users_code(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with a forgot password that belongs to a different user results in a 500 status code.
        """
        response: Response = self.client.post('/v2/forgot_password/andy')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response_json.get('created'))

        response: Response = self.client.get(
            '/v2/forgot_password/andy',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        forgot_password_codes = response_json.get('forgot_password_codes')
        self.assertGreaterEqual(len(forgot_password_codes), 1)

        request_body = json.dumps({
            "forgot_password_code": forgot_password_codes[0].get('forgot_code'),
            "new_password": "abcd1234"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), False)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), False)
        self.assertEqual(
            response_json.get('error'),
            "This forgot password code does not belong to the specified user."
        )

    def test_user_change_password_by_username_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with the proper fields results in a 200 status code.
        """
        response: Response = self.client.post('/v2/forgot_password/andy2')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response_json.get('created'))

        auth_url = self.auth_url

        async def token(test_suite: TestSuite):
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=f"{auth_url}/token",
                        json={'clientId': 'andy2', 'clientSecret': 'B0unDTw0'}
                ) as auth_response:
                    response_body = await auth_response.json()
                    test_suite.andy2_jwt = response_body.get('result')

        self.andy2_jwt = None
        asyncio.run(token(self))

        response: Response = self.client.get(
            '/v2/forgot_password/andy2',
            headers={'Authorization': f'Bearer {self.andy2_jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        forgot_password_codes = response_json.get('forgot_password_codes')
        self.assertGreaterEqual(len(forgot_password_codes), 1)

        request_body = json.dumps({
            "forgot_password_code": forgot_password_codes[0].get('forgot_code'),
            "new_password": "B0unDTw0"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), True)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), True)

    @unittest.skip('Password Change Does Not Require Authorization')
    def test_user_change_password_by_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/users/<username>/change_password' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy/change_password', AuthVariant.FORBIDDEN)

    @unittest.skip('Password Change Does Not Require Authorization')
    def test_user_change_password_by_username_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/users/<username>/change_password' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy/change_password', AuthVariant.UNAUTHORIZED)

    def test_user_update_last_login_by_username_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/update_last_login' route.  This test proves
        that calling this endpoint with the proper fields results in a 200 status code.
        """
        response: Response = self.client.put(
            '/v2/users/andy/update_last_login',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy/update_last_login')
        self.assertEqual(response_json.get('last_login_updated'), True)

    def test_user_update_last_login_by_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/users/<username>/update_last_login' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy/update_last_login', AuthVariant.FORBIDDEN)

    def test_user_update_last_login_by_username_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/users/<username>/update_last_login' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy/update_last_login', AuthVariant.UNAUTHORIZED)

    def test_user_lookup_by_username_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/lookup/<username>' route.  This test proves
        that looking for a user with a username that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/users/lookup/invalid_username')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/lookup/invalid_username')
        self.assertFalse(response_json.get('exists'))
        self.assertEqual(response_json.get('error'), 'There is no user with this username or email.')

    def test_user_lookup_by_username_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/lookup/<username>' route.  This test proves that
        looking for a user with a valid username results in a 200 status.
        """
        response: Response = self.client.get('/v2/users/lookup/andy')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/lookup/andy')
        self.assertTrue(response_json.get('exists'))

    def test_user_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/links' route.  This test proves that calling
        this endpoint returns a list of other user endpoints.
        """
        response: Response = self.client.get('/v2/users/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/links')
        self.assertEqual(len(response_json.get('endpoints')), 17)
