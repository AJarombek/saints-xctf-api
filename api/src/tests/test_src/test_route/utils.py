"""
Utility functions which assist in testing the routes in the Flask application.
Author: Andrew Jarombek
Date: 10/15/2020
"""

from unittest import TestCase, TestSuite
from enum import Enum

import aiohttp
from flask import Response
from flask.testing import FlaskClient


class AuthVariant(Enum):
    UNAUTHORIZED = 401, 'Unauthorized'
    FORBIDDEN = 403, 'Forbidden'


def test_route_auth(case: TestCase, client: FlaskClient, verb: str, endpoint: str, variant: AuthVariant) -> None:
    """
    Test making an API call to a route without a proper JWT token in the Authorization header.  This route should
    return a 401/403 HTTP code.
    :param case: Unittest test case from which to make assertions.
    :param client: Flask client for making HTTP requests.
    :param verb: The HTTP verb of the request to make.
    :param endpoint: Path of the endpoint on the API domain.
    :param variant: The condition to test.
    """
    if variant == AuthVariant.FORBIDDEN:
        headers = {'Authorization': ''}
    else:
        headers = {}

    if verb == 'GET':
        response: Response = client.get(endpoint, headers=headers)
    elif verb == 'POST':
        response: Response = client.post(endpoint, headers=headers)
    elif verb == 'PUT':
        response: Response = client.put(endpoint, headers=headers)
    elif verb == 'DELETE':
        response: Response = client.delete(endpoint, headers=headers)
    else:
        case.fail(f"Unexpected HTTP Verb: {verb}")
        return

    expected_code, expected_description = variant.value
    response_json: dict = response.get_json()
    case.assertEqual(expected_code, response.status_code)
    case.assertEqual(expected_description, response_json.get('error_description'))


async def get_jwt_token(test_suite: TestSuite, auth_url: str, client_id: str, client_secret: str):
    """
    Using an authentication URL, retrieve a JWT for a user to use in tests.
    :param test_suite: The test suite which needs the JWT.
    :param auth_url: The authentication URL to use.
    :param client_id: Username of the user that the JWT will belong to.
    :param client_secret: Password of the user that the JWT will belong to.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f"{auth_url}/token",
                json={'clientId': client_id, 'clientSecret': client_secret}
        ) as auth_response:
            response_body = await auth_response.json()
            test_suite.jwts[client_id] = response_body.get('result')
