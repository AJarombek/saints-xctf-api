"""
Test suite for the API routes that handle range view objects (api/src/route/userRoute.py).
Author: Andrew Jarombek
Date: 12/10/2019
"""

import json
from datetime import datetime

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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/users/', headers.get('Location'))

    def test_user_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/users' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users', AuthVariant.FORBIDDEN)

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
            headers={'Authorization': 'Bearer j.w.t'}
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
        self.assertNotIn('profilepic_name', user)
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
        self.assertTrue(user.get('deleted') is None or type(user.get('deleted')) is str)

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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
        self.client.delete(
            '/v2/activation_code/ABC123',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        request_body = json.dumps({'activation_code': 'ABC123'})
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
        self.assertEqual(response_json.get('activation_code'), {'activation_code': 'ABC123', 'deleted': None})

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy2',
            headers={'Authorization': 'Bearer j.w.t'}
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
            "activation_code": "ABC123",
            "last_signin": str(datetime.fromisoformat('2019-12-14'))
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
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
        self.assertNotIn('profilepic_name', user)
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

    def test_user_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/users/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/users/', AuthVariant.FORBIDDEN)

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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/users/invalid_username')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('user'))
        self.assertEqual(response_json.get('error'), 'there is no existing user with this username')

    def test_user_by_username_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>' route.  This test proves that
        if the updated user is the same as the original user, a 400 error is returned.
        """
        response: Response = self.client.get(
            '/v2/users/andy',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('user'))

        request_body = json.dumps(response_json.get('user'))

        response: Response = self.client.put(
            '/v2/users/andy',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy')
        self.assertTrue(response_json.get('updated'))
        self.assertIsNotNone(response_json.get('user'))

        # Confirm the fields were updated as expected.
        self.assertNotIn('profilepic', response_json.get('user'))
        self.assertNotIn('profilepic_name', response_json.get('user'))
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

    def test_user_by_username_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/<username>' route.  This test proves
        that the endpoint should return a 204 success status, no matter if the user existed or not.
        """
        response: Response = self.client.delete(
            '/v2/users/invalid_user',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(response.status_code, 204)

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
            headers={'Authorization': 'Bearer j.w.t'}
        )

        response: Response = self.client.delete(
            '/v2/users/soft/invalid_user',
            headers={'Authorization': 'Bearer j.w.t'}
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
        self.client.delete(
            '/v2/activation_code/DEFGHI',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        request_body = json.dumps({'activation_code': 'DEFGHI'})
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
        self.assertEqual(response_json.get('activation_code'), {'activation_code': 'DEFGHI', 'deleted': None})

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy3',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        request_body = json.dumps({
            "username": "andy3",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "password",
            "activation_code": "DEFGHI"
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        username = response_json.get('user').get('username')

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        self.assertEqual(response.status_code, 400)

    def test_user_by_username_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/users/soft/<username>' route.  This test proves that
        soft deleting an existing non-soft deleted user will execute successfully and return a valid 204 status.
        """
        # Before trying to create the user, make sure that the activation code already exists.
        self.client.delete(
            '/v2/activation_code/DEFGHI',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        request_body = json.dumps({'activation_code': 'DEFGHI'})
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
        self.assertEqual(response_json.get('activation_code'), {'activation_code': 'DEFGHI', 'deleted': None})

        # Delete the user to void a duplicate entry constraint error.
        self.client.delete(
            '/v2/users/andy3',
            headers={'Authorization': 'Bearer j.w.t'}
        )

        request_body = json.dumps({
            "username": "andy3",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "password",
            "activation_code": "DEFGHI"
        })

        response: Response = self.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        username = response_json.get('user').get('username')

        response: Response = self.client.delete(
            f'/v2/users/soft/{username}',
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
            headers={'Authorization': 'Bearer j.w.t'}
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
        self.assertNotIn('profilepic_name', user)
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
        self.assertTrue(user.get('deleted') is None or type(user.get('deleted')) is str)

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
        self.assertIn('miles', statistics)
        self.assertTrue(statistics.get('miles') is None or type(statistics.get('miles')) is float)
        self.assertIn('milespastmonth', statistics)
        self.assertTrue(statistics.get('milespastmonth') is None or type(statistics.get('milespastmonth')) is float)
        self.assertIn('milespastweek', statistics)
        self.assertTrue(statistics.get('milespastweek') is None or type(statistics.get('milespastweek')) is float)
        self.assertIn('milespastyear', statistics)
        self.assertTrue(statistics.get('milespastyear') is None or type(statistics.get('milespastyear')) is float)
        self.assertIn('runmiles', statistics)
        self.assertTrue(statistics.get('runmiles') is None or type(statistics.get('runmiles')) is float)
        self.assertIn('runmilespastyear', statistics)
        self.assertTrue(statistics.get('runmilespastyear') is None or type(statistics.get('runmilespastyear')) is float)
        self.assertIn('runmilespastmonth', statistics)
        self.assertTrue(statistics.get('runmilespastmonth') is None or type(statistics.get('runmilespastmonth')) is float)
        self.assertIn('runmilespastweek', statistics)
        self.assertTrue(statistics.get('runmilespastweek') is None or type(statistics.get('runmilespastweek')) is float)
        self.assertIn('alltimefeel', statistics)
        self.assertTrue(statistics.get('alltimefeel') is None or type(statistics.get('alltimefeel')) is float)
        self.assertIn('yearfeel', statistics)
        self.assertTrue(statistics.get('yearfeel') is None or type(statistics.get('yearfeel')) is float)
        self.assertIn('monthfeel', statistics)
        self.assertTrue(statistics.get('monthfeel') is None or type(statistics.get('monthfeel')) is float)
        self.assertIn('weekfeel', statistics)
        self.assertTrue(statistics.get('weekfeel') is None or type(statistics.get('weekfeel')) is float)

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

    def test_user_change_password_by_username_put_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with missing required fields results in a 400 error.
        """
        # Missing the required 'new_password' field
        request_body = json.dumps({
            "forgot_password_code": "123456"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), False)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), False)
        self.assertEqual(
            response_json.get('error'),
            "'forgot_password_code' and 'new_password' are required fields"
        )

    def test_user_change_password_by_username_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/users/<username>/change_password' route.  This test proves that
        calling this endpoint with the proper fields results in a 200 status code.
        """
        request_body = json.dumps({
            "forgot_password_code": "123456",
            "new_password": "B0unDTw0"
        })

        response: Response = self.client.put(
            '/v2/users/andy2/change_password',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/change_password')
        self.assertEqual(response_json.get('password_updated'), True)
        self.assertEqual(response_json.get('forgot_password_code_deleted'), True)

    def test_user_change_password_by_username_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/users/<username>/change_password' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/users/andy/change_password', AuthVariant.FORBIDDEN)

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
            '/v2/users/andy2/update_last_login',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/andy2/update_last_login')
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

    def test_user_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/users/links' route.  This test proves that calling
        this endpoint returns a list of other user endpoints.
        """
        response: Response = self.client.get('/v2/users/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/users/links')
        self.assertEqual(len(response_json.get('endpoints')), 13)
