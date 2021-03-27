"""
Test suite for the API routes that handle user notifications (api/src/route/notificationRoute.py).
Author: Andrew Jarombek
Date: 12/2/2019
"""

import json
from datetime import datetime

import asyncio
from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant, get_jwt_token


class TestNotificationRoute(TestSuite):

    def test_notification_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications' route. This route is redirected to
        '/v2/notifications/' by default.
        """
        response: Response = self.client.get(
            '/v2/notifications',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/notifications/', headers.get('Location'))

    def test_notification_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/notifications' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications', AuthVariant.FORBIDDEN)

    def test_notification_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/notifications' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications', AuthVariant.UNAUTHORIZED)

    def test_notification_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/notifications' route. This route is redirected to
        '/v2/notifications/' by default.
        """
        response: Response = self.client.post(
            '/v2/notifications',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/notifications/', headers.get('Location'))

    def test_notification_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/notifications' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/notifications', AuthVariant.FORBIDDEN)

    def test_notification_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/notifications' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/notifications', AuthVariant.UNAUTHORIZED)

    def test_notification_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/' route.  This test proves that the endpoint
        returns a list of notifications.
        """
        response: Response = self.client.get(
            '/v2/notifications/',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications')
        self.assertGreater(len(response_json.get('notifications')), 1)

        self.assertIn('notification_id', response_json.get('notifications')[0])
        notification = response_json.get('notifications')[0]

        self.assertIsInstance(notification.get('notification_id'), int)
        self.assertIn('username', response_json.get('notifications')[0])
        self.assertIsInstance(notification.get('username'), str)
        self.assertIn('time', response_json.get('notifications')[0])
        self.assertIsInstance(notification.get('time'), str)
        self.assertIn('link', response_json.get('notifications')[0])
        self.assertTrue(notification.get('link') is None or type(notification.get('link')) is str)
        self.assertIn('viewed', response_json.get('notifications')[0])
        self.assertIsInstance(notification.get('viewed'), str)
        self.assertIn('description', response_json.get('notifications')[0])
        self.assertTrue(notification.get('description') is None or type(notification.get('description')) is str)
        self.assertIn('deleted', response_json.get('notifications')[0])
        self.assertIsInstance(notification.get('deleted'), bool)

    def test_notification_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/notifications/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications/', AuthVariant.FORBIDDEN)

    def test_notification_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/notifications/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications/', AuthVariant.UNAUTHORIZED)

    def test_notification_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/notifications/' route.  This test proves that calling this
        endpoint with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post(
            '/v2/notifications/',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/notifications')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_notification_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/notifications/' route.  This test proves that calling this
        endpoint with missing required fields results in a 400 error.
        """
        # Missing the required 'time' field
        request_body = json.dumps({
            "username": "andy"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/notifications')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(
            response_json.get('error'),
            "'username' and 'description' are required fields"
        )

    def test_notification_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/notifications/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new notification object.
        """
        request_body = json.dumps({
            "username": "andy",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "Valid Notification"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('notification'))
        self.assertIn('notification_id', response_json.get('notification'))
        self.assertIn('username', response_json.get('notification'))
        self.assertIn('time', response_json.get('notification'))
        self.assertIn('link', response_json.get('notification'))
        self.assertIn('viewed', response_json.get('notification'))
        self.assertIn('description', response_json.get('notification'))
        self.assertIn('deleted', response_json.get('notification'))

    def test_notification_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/notifications/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/notifications/', AuthVariant.FORBIDDEN)

    def test_notification_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/notifications/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/notifications/', AuthVariant.UNAUTHORIZED)

    def test_notification_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/<notification_id>' route.  This test proves
        that trying to retrieve a notification with an ID that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            '/v2/notifications/0',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/notifications/0')
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(response_json.get('error'), 'there is no notification with this identifier')

    def test_notification_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/<notification_id>' route.  This test proves that
        retrieving a message with a valid ID results in the message and a 200 status.
        """
        response: Response = self.client.get(
            '/v2/notifications/1',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications/1')
        self.assertIsNotNone(response_json.get('notification'))

    def test_notification_by_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications/1', AuthVariant.FORBIDDEN)

    def test_notification_by_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/notifications/1', AuthVariant.UNAUTHORIZED)

    def test_notification_by_id_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/notifications/<notification_id>' route.  This test proves that
        trying to update a notification that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put(
            '/v2/notifications/0',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/notifications/0')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(response_json.get('error'), 'there is no existing notification with this id')

    def test_notification_by_id_put_route_400_other_users_notification(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/notifications/<notification_id>' route.  This test proves that
        trying to update a notification that doesn't belong to the user making the API call results in a 400 error.
        """
        request_body = json.dumps({
            "username": "andy2",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "Other User's Notification"
        })

        asyncio.run(get_jwt_token(test_suite=self, auth_url=self.auth_url, client_id='andy2', client_secret='B0unDTw0'))

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f"Bearer {self.jwts.get('andy2')}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('notification_id', response_json.get('notification'))
        notification_id = response_json.get('notification').get('notification_id')

        request_body = json.dumps(response_json.get('notification'))

        response: Response = self.client.put(
            f'/v2/notifications/{notification_id}',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), f'/v2/notifications/{notification_id}')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(
            response_json.get('error'),
            'User andy is not authorized to update a notification sent to andy2.'
        )

    def test_notification_by_id_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/notifications/<notification_id>' route.  This test proves that
        if the updated notification is the same as the original notification, a 400 error is returned.
        """
        request_body = json.dumps({
            "username": "andy",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "My Notification"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('notification_id', response_json.get('notification'))
        notification_id = response_json.get('notification').get('notification_id')

        response: Response = self.client.get(
            f'/v2/notifications/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('notification'))

        request_body = json.dumps(response_json.get('notification'))

        response: Response = self.client.put(
            f'/v2/notifications/{notification_id}',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), f'/v2/notifications/{notification_id}')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual(
            response_json.get('error'),
            'the notification submitted is equal to the existing notification with the same id'
        )

    def test_notification_by_id_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/notifications/<notification_id>' route.  This test proves that
        if a valid notification JSON is passed to this endpoint, the existing notification will be updated and a valid
        200 response code will be returned.
        """
        # 'viewed' is the only notification column that can be altered after creation.
        request_body = json.dumps({
            "username": "andy",
            "time": "2017-07-01 21:00:21",
            "link": "https://www.saintsxctf.com/log.php?logno=2017",
            "viewed": "Y",
            "description": f"Caroline Driscoll Commented on Your Log:."
        })

        response: Response = self.client.put(
            '/v2/notifications/29',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications/29')
        self.assertTrue(response_json.get('updated'))
        self.assertIsNotNone(response_json.get('notification'))
        self.assertIn('viewed', response_json.get('notification'))
        self.assertEqual(response_json.get('notification').get('viewed'), 'Y')

    def test_notification_by_id_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/notifications/1', AuthVariant.FORBIDDEN)

    def test_notification_by_id_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/notifications/1', AuthVariant.UNAUTHORIZED)

    def test_notification_by_id_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/<notification_id>' route.  This test proves
        that the endpoint should return a 400 error status if the notification id specified does not exist.
        """
        response: Response = self.client.delete(
            '/v2/notifications/0',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual('There is no existing notification with this id.', response_json.get('error'))

    def test_notification_by_id_delete_route_400_other_users_notification(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/<notification_id>' route.  This test proves
        that the endpoint should return a 400 error status if the notification belongs to another user.
        """
        request_body = json.dumps({
            "username": "andy2",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "Other User's Notification"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('notification_id', response_json.get('notification'))
        notification_id = response_json.get('notification').get('notification_id')

        response: Response = self.client.delete(
            f'/v2/notifications/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual(
            'User andy is not authorized to delete a notification sent to andy2.',
            response_json.get('error')
        )

    def test_notification_by_id_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/<notification_id>' route.  This test proves
        that the endpoint should return a 204 success status, no matter if the notification existed or not.
        """
        request_body = json.dumps({
            "username": "andy",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "My Notification"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('notification_id', response_json.get('notification'))
        notification_id = response_json.get('notification').get('notification_id')

        response: Response = self.client.delete(
            f'/v2/notifications/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

    def test_notification_by_id_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/notifications/1', AuthVariant.FORBIDDEN)

    def test_notification_by_id_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/notifications/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/notifications/1', AuthVariant.UNAUTHORIZED)

    def test_notification_by_id_soft_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.  This test
        proves that if the notification doesn't exist, a 400 error is returned.
        """
        # Ensure that the notification was already deleted before testing the DELETE endpoint
        self.client.delete(
            '/v2/notifications/0',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )

        response: Response = self.client.delete(
            '/v2/notifications/soft/0',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))

    def test_notification_by_id_soft_delete_route_400_other_users_notification(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.  This test
        proves that if the notification belongs to another user, a 400 error is returned.
        """
        request_body = json.dumps({
            "username": "andy2",
            "viewed": "N",
            "time": str(datetime.now()),
            "description": "Other User's Notification"
        })

        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('notification_id', response_json.get('notification'))
        notification_id = response_json.get('notification').get('notification_id')

        response: Response = self.client.delete(
            f'/v2/notifications/soft/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))
        self.assertEqual(
            'User andy is not authorized to soft delete a notification sent to andy2.',
            response_json.get('error')
        )

    def test_notification_by_id_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.  This test
        proves that if the notification was already soft deleted, a 400 error is returned.
        """
        # Ensure that the notification was already soft deleted before testing the DELETE endpoint
        request_body = json.dumps({
            "username": "andy",
            "time": "2019-12-05 20:00:00",
            "link": "https://www.saintsxctf.com/",
            "viewed": "N",
            "description": "I hope you have a wonderful weekend.  This is our busiest two days selling Christmas Trees",
            "deleted": False
        })
        response: Response = self.client.post(
            '/v2/notifications/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        notification_id = response_json.get('notification').get('notification_id')

        response: Response = self.client.delete(
            f'/v2/notifications/soft/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.delete(
            f'/v2/notifications/soft/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_notification_by_id_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.  This test
        proves that soft deleting an existing non-soft deleted notification will execute successfully and return a
        valid 204 status.
        """
        # Ensure that the notification exists before testing the soft DELETE endpoint
        request_body = json.dumps({
            "username": "andy",
            "time": "2019-12-05 22:00:00",
            "link": "https://www.saintsxctf.com/",
            "viewed": "N",
            "description": "You mean so much to me, so of course whatever you are capable of I will reciprocate back " +
                           "to you.  You never have to worry about that.  Take your time and do what makes you happy.",
            "deleted": False
        })
        response: Response = self.client.post(
            '/v2/notifications/', data=request_body, content_type='application/json',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        notification_id = response_json.get('notification').get('notification_id')

        response = self.client.delete(
            f'/v2/notifications/soft/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.get(
            f'/v2/notifications/{notification_id}',
            headers={'Authorization': f'Bearer {self.jwt}'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response_json.get('notification'))
        self.assertEqual('there is no notification with this identifier', response_json.get('error'))

    def test_notification_by_id_soft_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/notifications/soft/1', AuthVariant.FORBIDDEN)

    def test_notification_by_id_soft_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/notifications/soft/<notification_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/notifications/soft/1', AuthVariant.UNAUTHORIZED)

    def test_notification_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/notifications/links' route.  This test proves that calling
        this endpoint returns a list of other notification endpoints.
        """
        response: Response = self.client.get('/v2/notifications/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/notifications/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
