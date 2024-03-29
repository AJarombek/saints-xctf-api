"""
Test suite for the API routes that handle comments on logs (api/src/route/commentRoute.py)
Author: Andrew Jarombek
Date: 10/11/2019
"""

import json
from datetime import datetime

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestCommentRoute(TestSuite):
    def test_comment_get_route_redirect(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.get(
            "/v2/comments", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 302)
        self.assertIn("/v2/comments/", headers.get("Location"))

    def test_comment_get_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/comments' route.
        """
        test_route_auth(self, self.client, "GET", "/v2/comments", AuthVariant.FORBIDDEN)

    def test_comment_get_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/comments' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/comments", AuthVariant.UNAUTHORIZED
        )

    def test_comment_post_route_redirect(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments' route. This route is redirected to
        '/v2/comments/' by default.
        """
        response: Response = self.client.post(
            "/v2/comments", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        headers = response.headers
        self.assertEqual(response.status_code, 307)
        self.assertIn("/v2/comments/", headers.get("Location"))

    def test_comment_post_route_redirect_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/comments' route.
        """
        test_route_auth(
            self, self.client, "POST", "/v2/comments", AuthVariant.FORBIDDEN
        )

    def test_comment_post_route_redirect_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/comments' route.
        """
        test_route_auth(
            self, self.client, "POST", "/v2/comments", AuthVariant.UNAUTHORIZED
        )

    def test_comment_get_all_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/' route.  This test proves that the endpoint returns
        a list of comments.
        """
        response: Response = self.client.get(
            "/v2/comments/", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertGreater(len(response_json.get("comments")), 1)

    def test_comment_get_all_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/comments/' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/comments/", AuthVariant.FORBIDDEN
        )

    def test_comment_get_all_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/comments/' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/comments/", AuthVariant.UNAUTHORIZED
        )

    def test_comment_post_route_400_empty_body(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling this endpoint
        with an empty request body results in a 400 error code.
        """
        response: Response = self.client.post(
            "/v2/comments/", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertEqual(response_json.get("added"), False)
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(response_json.get("error"), "the request body isn't populated")

    def test_comment_post_route_400_missing_required_field(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling this endpoint
        with missing required fields results in a 400 error.
        """
        request_body = json.dumps(
            {"username": "andy", "first": "Andrew", "last": "Jarombek"}
        )

        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertEqual(response_json.get("added"), False)
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(
            response_json.get("error"),
            "'username', 'first', 'last', and 'log_id' are required fields",
        )

    def test_comment_post_route_400_other_user(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 400 success code if a user is attempting to create a
        comment for another user.
        """
        request_body = json.dumps(
            {
                "username": "andy2",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2021-03-27 12:00:00",
                "content": "Hi",
            }
        )

        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertFalse(response_json.get("added"))
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to create a comment for user andy2.",
        )

    def test_comment_post_route_200(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/comments/' route.  This test proves that calling
        this endpoint with a valid request JSON results in a 200 success code and a new comment object.
        """
        request_body = json.dumps(
            {
                "username": "andy",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2019-10-20 13:10:50",
                "content": "Hi",
            }
        )

        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertEqual(response_json.get("added"), True)
        self.assertIsNotNone(response_json.get("comment"))

    def test_comment_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/comments/' route.
        """
        test_route_auth(
            self, self.client, "POST", "/v2/comments/", AuthVariant.FORBIDDEN
        )

    def test_comment_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/comments/' route.
        """
        test_route_auth(
            self, self.client, "POST", "/v2/comments/", AuthVariant.UNAUTHORIZED
        )

    def test_comment_with_id_get_route_400(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/<comment_id>' route.  This test proves that trying to
        retrieve a comment with an ID that doesn't exist results in a HTTP 400 error.
        """
        response: Response = self.client.get(
            "/v2/comments/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/0")
        self.assertIsNone(response_json.get("comment"))
        self.assertIsNone(response_json.get("log"))
        self.assertEqual(
            response_json.get("error"), "there is no comment with this identifier"
        )

    def test_comment_with_id_get_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/<comment_id>' route.  This test proves that retrieving
        a comment with a valid ID results in the comment and a 200 status.
        """
        response: Response = self.client.get(
            "/v2/comments/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments/1")
        self.assertIsNotNone(response_json.get("comment"))
        self.assertEqual(response_json.get("log"), "/v2/logs/1")

    def test_comment_with_id_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/comments/1", AuthVariant.FORBIDDEN
        )

    def test_comment_with_id_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/comments/1", AuthVariant.UNAUTHORIZED
        )

    def test_comment_with_id_put_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/comments/<comment_id>' route.  This test proves that trying to
        update a comment that doesn't exist results in a 400 error.
        """
        response: Response = self.client.put(
            "/v2/comments/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/0")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(
            response_json.get("error"), "there is no existing comment with this id"
        )

    def test_comment_with_id_put_route_400_no_update(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/comments/<comment_id>' route.  This test proves that if the
        updated comment is the same as the original comment, a 400 error is returned.
        """
        response: Response = self.client.get(
            "/v2/comments/1", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json.get("comment"))

        request_body = json.dumps(response_json.get("comment"))

        response: Response = self.client.put(
            "/v2/comments/1",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/1")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(
            response_json.get("error"),
            "the comment submitted is equal to the existing comment with the same id",
        )

    def test_comment_with_id_put_route_400_other_user(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/comments/<comment_id>' route.  This test proves that if a valid
        comment JSON is passed to this endpoint, a 400 error response code will be returned if a user is attempting to
        edit another users comment.
        """
        request_body = json.dumps(
            {
                "comment_id": 2,
                "username": "dotty",
                "first": "Dotty",
                "last": "J",
                "log_id": 1,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": f"Keep up the good work!! (Edited {datetime.now()})",
            }
        )

        response: Response = self.client.put(
            "/v2/comments/2",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/2")
        self.assertFalse(response_json.get("updated"))
        self.assertIsNone(response_json.get("comment"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to update a comment with id 2.",
        )

    def test_comment_with_id_put_route_200(self) -> None:
        """
        Test performing an HTTP PUT request on the '/v2/comments/<comment_id>' route.  This test proves that if a valid
        comment JSON is passed to this endpoint, the existing comment will be updated and a valid 200 response code
        will be returned.
        """
        request_body = json.dumps(
            {
                "comment_id": 1,
                "username": "andy",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2016-12-23 21:32:42",
                "content": f"First Comment! (Edited {datetime.now()})",
                "deleted": False,
            }
        )

        response: Response = self.client.put(
            "/v2/comments/1",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments/1")
        self.assertTrue(response_json.get("updated"))
        self.assertIsNotNone(response_json.get("comment"))

    def test_comment_with_id_put_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP PUT request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "PUT", "/v2/comments/1", AuthVariant.FORBIDDEN
        )

    def test_comment_with_id_put_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP PUT request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "PUT", "/v2/comments/1", AuthVariant.UNAUTHORIZED
        )

    def test_comment_with_id_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/<comment_id>' route.  This test proves that the
        endpoint should return a 400 error status if the comment does not exist.
        """
        response: Response = self.client.delete(
            "/v2/comments/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/0")
        self.assertFalse(response_json.get("deleted"))
        self.assertEqual(
            response_json.get("error"), "there is no existing comment with this id"
        )

    def test_comment_with_id_delete_route_400_other_user(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/<comment_id>' route.  This test proves that the
        endpoint should return a 400 error status, no matter if the code existed or not.
        """
        response: Response = self.client.delete(
            "/v2/comments/2", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/2")
        self.assertFalse(response_json.get("deleted"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to delete a comment with id 2.",
        )

    def test_comment_with_id_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/<comment_id>' route.  This test proves that the
        endpoint should return a 204 success status, no matter if the code existed or not.
        """
        request_body = json.dumps(
            {
                "username": "andy",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2021-03-27 12:00:00",
                "content": "I hope you are having a nice weekend.",
            }
        )

        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertEqual(response_json.get("added"), True)
        self.assertIsNotNone(response_json.get("comment"))
        comment_id = response_json.get("comment").get("comment_id")

        response: Response = self.client.delete(
            f"/v2/comments/{comment_id}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        self.assertEqual(response.status_code, 204)

    def test_comment_with_id_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "DELETE", "/v2/comments/1", AuthVariant.FORBIDDEN
        )

    def test_comment_with_id_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/comments/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "DELETE", "/v2/comments/1", AuthVariant.UNAUTHORIZED
        )

    def test_comment_with_id_soft_delete_route_204(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.  This test proves that
        soft deleting an existing non-soft deleted comment will execute successfully and return a valid 204 status.
        """
        # Ensure that the comment exists before testing the soft DELETE endpoint
        request_body = json.dumps(
            {
                "username": "andy",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2019-10-26 20:00:00",
                "content": "Comment to be soft deleted",
                "deleted": False,
            }
        )
        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        comment_id = response_json.get("comment").get("comment_id")

        response = self.client.delete(
            f"/v2/comments/soft/{comment_id}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        self.assertEqual(response.status_code, 204)

    def test_comment_with_id_soft_delete_route_400_no_existing(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.  This test proves that if
        the comment doesn't exist, a 400 error is returned.
        """
        # Ensure that the comment was already deleted before testing the DELETE endpoint
        self.client.delete(
            "/v2/comments/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )

        response: Response = self.client.delete(
            "/v2/comments/soft/0", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get("deleted"))

    def test_comment_with_id_soft_delete_route_400_already_deleted(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.  This test proves that if
        the comment was already soft deleted, a 400 error is returned.
        """
        # Ensure that the comment was already soft deleted before testing the DELETE endpoint
        request_body = json.dumps(
            {
                "username": "andy",
                "first": "Andrew",
                "last": "Jarombek",
                "log_id": 1,
                "time": "2021-01-24 13:10:50",
                "content": "Hi",
            }
        )

        response: Response = self.client.post(
            "/v2/comments/",
            data=request_body,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )

        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments")
        self.assertEqual(response_json.get("added"), True)

        comment_response: dict = response_json.get("comment")
        self.assertIsNotNone(comment_response)
        comment_id = comment_response.get("comment_id")

        response = self.client.delete(
            f"/v2/comments/soft/{comment_id}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        self.assertEqual(response.status_code, 204)

        response: Response = self.client.delete(
            f"/v2/comments/soft/{comment_id}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json.get("deleted"))

    def test_comment_with_id_soft_delete_route_400_other_user(self) -> None:
        """
        Test performing an HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.  This test proves that the
        endpoint should return a 400 error status, no matter if the code existed or not.
        """
        response: Response = self.client.delete(
            "/v2/comments/soft/2", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/comments/soft/2")
        self.assertFalse(response_json.get("deleted"))
        self.assertEqual(
            response_json.get("error"),
            "User andy is not authorized to soft delete a comment with id 2.",
        )

    def test_comment_with_id_soft_delete_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "DELETE", "/v2/comments/soft/1", AuthVariant.FORBIDDEN
        )

    def test_comment_with_id_soft_delete_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP DELETE request on the '/v2/comments/soft/<comment_id>' route.
        """
        test_route_auth(
            self, self.client, "DELETE", "/v2/comments/soft/1", AuthVariant.UNAUTHORIZED
        )

    def test_comment_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/comments/links' route.  This test proves that calling
        this endpoint returns a list of other comment endpoints.
        """
        response: Response = self.client.get("/v2/comments/links")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/comments/links")
        self.assertEqual(len(response_json.get("endpoints")), 6)
