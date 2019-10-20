"""
Test suite for the API routes that handle comments on logs (api/src/route/commentRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

import json
from flask import Response
from tests.TestSuite import TestSuite


class TestCommentRoute(TestSuite):

    def test_comment_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.post('/v2/comments')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/comments/', headers.get('Location'))

    def test_comment_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.post('/v2/comments')
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn('/v2/comments/', headers.get('Location'))

    def test_comment_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/' route.  This test proves that the endpoint returns
        a list of comments.
        """
        response: Response = self.client.get('/v2/comments/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/comments')
        self.assertGreater(len(response_json.get('comments')), 1)

    def test_comment_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post('/v2/comments/')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/comments')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('comment'))
        self.assertEqual(response_json.get('error'), "the request body isn't populated")

    def test_comment_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        request_body = json.dumps({"username": "andy", "first": "Andrew", "last": "Jarombek"})

        response: Response = self.client.post(
            '/v2/comments/',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/comments')
        self.assertEqual(response_json.get('added'), False)
        self.assertIsNone(response_json.get('comment'))
        self.assertEqual(
            response_json.get('error'),
            "'username', 'first', 'last', 'log_id', and 'time' are required fields"
        )

    def test_comment_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new comment object.
        """
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "log_id": 1,
            "time": "2019-10-20 13:10:50",
            "content": "Hi"
        })

        response: Response = self.client.post(
            '/v2/comments/',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/comments')
        self.assertEqual(response_json.get('added'), True)
        self.assertIsNotNone(response_json.get('comment'))

    def test_comment_with_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/<comment_id>' route.  This test proves that trying to
        retrieve a comment with an ID that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get('/v2/comments/0')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/comments/0')
        self.assertIsNone(response_json.get('comment'))
        self.assertIsNone(response_json.get('log'))
        self.assertEqual(response_json.get('error'), 'there is no comment with this identifier')

    def test_comment_with_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/<comment_id>' route.  This test proves that retrieving
        a comment with a valid ID results in the comment and a 200 status.
        """
        response: Response = self.client.get('/v2/comments/1')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/comments/1')
        self.assertIsNotNone(response_json.get('comment'))
        self.assertEqual(response_json.get('log'), '/v2/logs/1')

    def test_comment_with_id_put_route_400_no_existing(self) -> None:
        response: Response = self.client.put('/v2/comments/0')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/comments/0')
        self.assertFalse(response_json.get('updated'))
        self.assertIsNone(response_json.get('comment'))
        self.assertEqual(response_json.get('error'), 'there is no existing comment with this id')

    def test_comment_with_id_put_route_400_no_update(self) -> None:
        request_body = json.dumps({
            "username": "andy",
            "first": "Andrew",
            "last": "Jarombek",
            "log_id": 1,
            "time": "2016-12-23 21:32:42",
            "content": "First Log!"
        })

        response: Response = self.client.put(
            '/v2/comments/1',
            data=request_body,
            content_type='application/json'
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get('self'), '/v2/comments/1')

    def test_comment_with_id_put_route_200(self) -> None:
        pass

    def test_comment_with_id_delete_route_204(self) -> None:
        pass

    def test_comment_with_id_soft_delete_route_400_no_existing(self) -> None:
        pass

    def test_comment_with_id_soft_delete_route_400_already_deleted(self) -> None:
        pass

    def test_comment_with_id_soft_delete_route_200(self) -> None:
        pass

    def test_comment_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/links' route.  This test proves that calling
        this endpoint returns a list of other comment endpoints.
        """
        response: Response = self.client.get('/v2/comments/links')
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get('self'), '/v2/comments/links')
        self.assertEqual(len(response_json.get('endpoints')), 6)
