"""
Test suite for the API routes that handle forgot password codes assigned to a user
(api/src/route/forgotPasswordRoute.py)
Author: Andrew Jarombek
Date: 11/5/2019
"""

import unittest

from flask import Response

from tests.TestSuite import TestSuite
from tests.test_src.test_route.utils import test_route_auth, AuthVariant


class TestForgotPasswordRoute(TestSuite):
    def test_forgot_password_get_route_400_empty(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/<username>' route.  This test proves that
        trying to retrieve a forgot password code for a user that doesn't exist results in a HTTP 400 error code
        with an empty list returned.
        """
        response: Response = self.client.get(
            "/v2/forgot_password/fake_user",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/forgot_password/fake_user")
        self.assertEqual(response_json.get("forgot_password_codes"), [])

    def test_forgot_password_get_route_200_populated(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/<username>' route.  This test proves that
        trying to retrieve a forgot password code for a valid user with existing forgot password codes results in one
        or more forgot password codes and a successful HTTP 200 code.
        """
        # Ensure that at least one forgot password code exists for this user
        self.client.post(
            "/v2/forgot_password/andy", headers={"Authorization": f"Bearer {self.jwt}"}
        )

        response: Response = self.client.get(
            "/v2/forgot_password/andy", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/forgot_password/andy")
        self.assertGreaterEqual(len(response_json.get("forgot_password_codes")), 1)

    def test_forgot_password_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(
            self, self.client, "GET", "/v2/forgot_password/andy", AuthVariant.FORBIDDEN
        )

    def test_forgot_password_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/forgot_password/andy",
            AuthVariant.UNAUTHORIZED,
        )

    def test_forgot_password_post_route_400_invalid_user(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/forgot_password/<username>' route.  This test proves that
        calling this endpoint with a invalid username results in a 400 error code.
        """
        response: Response = self.client.post("/v2/forgot_password/fake_user")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json.get("self"), "/v2/forgot_password/fake_user")
        self.assertFalse(response_json.get("created"))
        self.assertEqual(
            response_json.get("error"),
            "There is no user associated with this username/email.",
        )

    def test_forgot_password_post_route_201(self) -> None:
        """
        Test performing an HTTP POST request on the '/v2/forgot_password/<username>' route.  This test proves that
        calling this endpoint with a valid username results in a new forgot password code being created.
        """
        response: Response = self.client.post("/v2/forgot_password/andy")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get("self"), "/v2/forgot_password/andy")
        self.assertTrue(response_json.get("created"))

    @unittest.skip("Forgot Password Code Creation Does Not Require Authorization")
    def test_forgot_password_post_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP POST request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(
            self, self.client, "POST", "/v2/forgot_password/andy", AuthVariant.FORBIDDEN
        )

    @unittest.skip("Forgot Password Code Creation Does Not Require Authorization")
    def test_forgot_password_post_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP POST request on the '/v2/forgot_password/<username>' route.
        """
        test_route_auth(
            self,
            self.client,
            "POST",
            "/v2/forgot_password/andy",
            AuthVariant.UNAUTHORIZED,
        )

    def test_forgot_password_code_validation_get_route_200_invalid(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/validate/<code>' route.  This test proves that
        validating a forgot password code that doesnt exist still results in a 200 HTTP code but has the is_valid field
        set to false.
        """
        response: Response = self.client.get(
            "/v2/forgot_password/validate/abc123",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json.get("self"), "/v2/forgot_password/validate/abc123"
        )
        self.assertFalse(response_json.get("is_valid"))

    def test_forgot_password_code_validation_get_route_200_valid(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/validate/<code>' route.  This test proves that
        validating a forgot password code that exists results in a 200 HTTP code response.
        """
        response: Response = self.client.post(
            "/v2/forgot_password/andy", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        self.assertEqual(response.status_code, 201)

        response: Response = self.client.get(
            "/v2/forgot_password/andy", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        forgot_password_codes = response_json.get("forgot_password_codes")
        self.assertGreaterEqual(len(forgot_password_codes), 1)

        forgot_password_code = forgot_password_codes[0].get("forgot_code")

        response: Response = self.client.get(
            f"/v2/forgot_password/validate/{forgot_password_code}"
        )
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json.get("self"),
            f"/v2/forgot_password/validate/{forgot_password_code}",
        )
        self.assertEqual(response_json.get("is_valid"), True)

    @unittest.skip("Forgot Password Code Validation Does Not Require Authorization")
    def test_forgot_password_code_validation_get_route_forbidden(self) -> None:
        """
        Test performing a forbidden HTTP GET request on the '/v2/forgot_password/validate/<code>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/forgot_password/validate/abc123",
            AuthVariant.FORBIDDEN,
        )

    @unittest.skip("Forgot Password Code Validation Does Not Require Authorization")
    def test_forgot_password_code_validation_get_route_unauthorized(self) -> None:
        """
        Test performing an unauthorized HTTP GET request on the '/v2/forgot_password/validate/<code>' route.
        """
        test_route_auth(
            self,
            self.client,
            "GET",
            "/v2/forgot_password/validate/abc123",
            AuthVariant.UNAUTHORIZED,
        )

    def test_forgot_password_get_links_route_200(self) -> None:
        """
        Test performing an HTTP GET request on the '/v2/forgot_password/links' route.  This test proves that calling
        this endpoint returns a list of other forgot password endpoints.
        """
        response: Response = self.client.get("/v2/forgot_password/links")
        response_json: dict = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json.get("self"), "/v2/forgot_password/links")
        self.assertEqual(len(response_json.get("endpoints")), 3)
