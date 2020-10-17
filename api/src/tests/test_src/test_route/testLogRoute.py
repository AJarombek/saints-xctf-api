"""
Test suite for the API routes that handle exercise logs (api/src/route/logRoute.py).
Author: Andrew Jarombek
Date: 11/17/2019
"""

import json
import unittest
from datetime import datetime

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestLogRoute(TestSuite):

    def test_log_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs' route. This route is redirected to
        '/v2/logs/' by default.
        """
        response: Response = self.client.get('/v2/logs', headers={'Authorization': 'Bearer j.w.t'})
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn('/v2/logs/', headers.get('Location'))

    def test_log_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/logs' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs', AuthVariant.FORBIDDEN)

    def test_log_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/logs' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs', AuthVariant.UNAUTHORIZED)

    def test_log_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs' route. This route is redirected to
        '/v2/logs/' by default.
        """
        response: Response = self.client.post('/v2/logs', headers={'Authorization': 'Bearer j.w.t'})
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/logs/', headers.get('Location'))

    def test_log_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/logs' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/logs', AuthVariant.FORBIDDEN)

    def test_log_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/logs' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/logs', AuthVariant.UNAUTHORIZED)

    @unittest.skip('Expensive Test')
    def test_log_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs/' route.  This test proves that the endpoint returns
        a list of logs.
        """
        response: Response = self.client.get('/v2/logs/', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertGreater(len(response_json.get('logs')), 1)

    def test_log_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/logs/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs/', AuthVariant.FORBIDDEN)

    def test_log_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/logs/' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs/', AuthVariant.UNAUTHORIZED)

    def test_log_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/logs/', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_log_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        # Missing the required 'date' field
        request_body = json.dumps({
            "log_id": 2,
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "type": "run",
            "feel": 6,
            "miles": 4.75,
            "time_created": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/logs/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(
            response_json.get('error'),
            "'username', 'first', 'last', 'date', 'type', and 'feel' are required fields"
        )

    def test_log_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/logs/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new log object.
        """
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "date": "2019-11-21",
            "type": "run",
            "feel": 6,
            "miles": 4.75,
            "time_created": str(datetime.now())
        })

        response: Response = self.client.post(
            '/v2/logs/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('log'))

    def test_log_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/logs/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/logs/', AuthVariant.FORBIDDEN)

    def test_log_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/logs/' route.
        """
        test_route_auth(self, self.client, 'POST', '/v2/logs/', AuthVariant.UNAUTHORIZED)

    def test_log_by_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs/<log_id>' route.  This test proves that trying to
        retrieve a log with an ID that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/logs/0', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs/0')
        self.assertIsNone(response_json.get('log'))
        self.assertIsNone(response_json.get('comments'))
        self.assertEqual(response_json.get('error'), 'there is no log with this identifier')

    def test_log_by_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs/<log_id>' route.  This test proves that retrieving
        a log with a valid ID results in the log and a 200 status.
        """
        response: Response = self.client.get('/v2/logs/1', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs/1')
        self.assertIsNotNone(response_json.get('log'))
        self.assertGreaterEqual(len(response_json.get('comments')), 1)

    def test_log_by_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs/1', AuthVariant.FORBIDDEN)

    def test_log_by_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'GET', '/v2/logs/1', AuthVariant.UNAUTHORIZED)

    def test_log_by_id_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/logs/<log_id>' route.  This test proves that trying to
        update a log that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put('/v2/logs/0', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs/0')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(response_json.get('error'), 'there is no existing log with this id')

    def test_log_by_id_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/logs/<log_id>' route.  This test proves that if the
        updated log is the same as the original log, a 400 error is returned.
        """
        response: Response = self.client.get('/v2/logs/1', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('log'))

        request_body = json.dumps(response_json.get('log'))

        response: Response = self.client.put(
            '/v2/logs/1',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/logs/1')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(
            response_json.get('error'),
            'the log submitted is equal to the existing log with the same id'
        )

    def test_log_by_id_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/logs/<log_id>' route.  This test proves that if a valid
        log JSON is passed to this endpoint, the existing log will be updated and a valid 200 response code
        will be returned.
        """
        request_body = json.dumps({
            "log_id": 1,
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "name": "Rockies",
            "location": "Sleepy Hollow, NY",
            "date": "2016-12-23",
            "type": "run",
            "distance": 8.5,
            "metric": "miles",
            "miles": 8.5,
            "time": "60:00:00",
            "pace": "00:07:04",
            "feel": 8,
            "description": f"Really nice run through the trails at night.  (Edited {datetime.now()})",
            "time_created": "0000-00-00 00:00:00",
            "deleted": None
        })

        response: Response = self.client.put(
            '/v2/logs/1',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs/1')
        self.assertTrue(response_json.get('updated'))
        self.assertIsNotNone(response_json.get('log'))

    def test_log_by_id_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/logs/1', AuthVariant.FORBIDDEN)

    def test_log_by_id_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'PUT', '/v2/logs/1', AuthVariant.UNAUTHORIZED)

    def test_log_by_id_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/logs/<log_id>' route.  This test proves that the
        endpoint should return a 204 success status, no matter if the log existed or not.
        """
        response: Response = self.client.delete('/v2/logs/0', headers={'Authorization': 'Bearer j.w.t'})
        self.assertEqual(response.status_code, 204)

    def test_log_by_id_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/logs/1', AuthVariant.FORBIDDEN)

    def test_log_by_id_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/logs/<log_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/logs/1', AuthVariant.UNAUTHORIZED)

    def test_log_by_id_soft_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/logs/soft/<log_id>' route.  This test proves that if
        the log doesn't exist, a 400 error is returned.
        """
        # Ensure that the log was already deleted before testing the DELETE endpoint
        self.client.delete('/v2/logs/0', headers={'Authorization': 'Bearer j.w.t'})

        response: Response = self.client.delete('/v2/logs/soft/0', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get('deleted'))

    def test_log_by_id_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/logs/soft/<comment_id>' route.  This test proves that if
        the comment was already soft deleted, a 400 error is returned.
        """
        # Ensure that the log was already soft deleted before testing the DELETE endpoint
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "name": "Bike Warmup",
            "location": "Riverside, CT",
            "date": "2019-11-23",
            "type": "bike",
            "time": "00:35:00",
            "feel": 5,
            "description": f"Loosen up my legs before running this morning, my knee hurt a little bit yesterday and I"
            f"want it to be healthy for the Manchester Road Race on Thursday.",
            "time_created": "2019-11-23 16:00:00",
            "deleted": 'Y'
        })
        response: Response = self.client.post(
            '/v2/logs/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        log_id = response_json.get('log').get('log_id')

        response: Response = self.client.delete(f'/v2/logs/soft/{log_id}', headers={'Authorization': 'Bearer j.w.t'})
        self.assertEqual(response.status_code, 400)

    def test_log_by_id_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/logs/soft/<log_id>' route.  This test proves that
        soft deleting an existing non-soft deleted log will execute successfully and return a valid 204 status.
        """
        # Ensure that the log exists before testing the soft DELETE endpoint
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "name": "Short Morning Run",
            "location": "Riverside, CT",
            "date": "2019-11-23",
            "type": "run",
            "distance": 2.3,
            "metric": "miles",
            "miles": 2.3,
            "time": "00:16:24",
            "pace": "00:07:08",
            "feel": 5,
            "description": f"Short run around the neighborhood after unloading Christmas trees this morning.",
            "time_created": "2019-11-23 15:00:00",
            "deleted": None
        })
        response: Response = self.client.post(
            '/v2/logs/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': 'Bearer j.w.t'}
        )
        response_json: dict = response.get_json()
        log_id = response_json.get('log').get('log_id')

        response = self.client.delete(f'/v2/logs/soft/{log_id}', headers={'Authorization': 'Bearer j.w.t'})
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.get(f'/v2/logs/{log_id}', headers={'Authorization': 'Bearer j.w.t'})
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get('log'))
        self.assertTrue(response_json.get('log').get('deleted'))

    def test_log_by_id_soft_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/logs/soft/<log_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/logs/soft/1', AuthVariant.FORBIDDEN)

    def test_log_by_id_soft_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/logs/soft/<log_id>' route.
        """
        test_route_auth(self, self.client, 'DELETE', '/v2/logs/soft/1', AuthVariant.UNAUTHORIZED)

    def test_log_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/logs/links' route.  This test proves that calling
        this endpoint returns a list of other log endpoints.
        """
        response: Response = self.client.get('/v2/logs/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/logs/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
