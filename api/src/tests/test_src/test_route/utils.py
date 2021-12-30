"""
Utility functions which assist in testing the routes in the Flask application.
Author: Andrew Jarombek
Date: 10/15/2020
"""

import string
import random
import json
from unittest import TestCase, TestSuite
from enum import Enum
from typing import Union, Any
from datetime import datetime

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


async def get_jwt_token(test_suite: Union[TestSuite, Any], auth_url: str, client_id: str, client_secret: str) -> None:
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


def random_code() -> str:
    """
    Create a random 12 digit code made up of latin characters and digits.
    :return: The 12 digit random code.
    """
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=12))


def create_test_user(case: TestCase) -> str:
    """
    Create a user which can be used for tests.
    :param case: Unittest test case from which to make assertions and access variables.
    :return: The username of the test user.
    """
    request_body = json.dumps({'email': 'andrew@jarombek.com', 'group_id': 1})
    response: Response = case.client.post(
        '/v2/activation_code/',
        data=request_body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {case.jwt}'}
    )

    response_json: dict = response.get_json()
    case.assertEqual(response.status_code, 200)
    case.assertEqual(response_json.get('self'), '/v2/activation_code')
    case.assertEqual(response_json.get('added'), True)

    activation_code_json = response_json.get('activation_code')
    activation_code = activation_code_json.get('activation_code')
    case.assertEqual(6, len(activation_code_json.get('activation_code')))
    case.assertEqual(1, activation_code_json.get('group_id'))
    case.assertEqual('andrew@jarombek.com', activation_code_json.get('email'))
    case.assertIn('expiration_date', activation_code_json)

    random_username = f'andy{random_code()}'
    request_body = json.dumps({
        "username": random_username,
        "email": "andrew@jarombek.com",
        "first": "Andrew",
        "last": "Jarombek",
        "password": "password",
        "activation_code": activation_code
    })

    response: Response = case.client.post(
        '/v2/users/',
        data=request_body,
        content_type='application/json',
        headers={'Authorization': f'Bearer {case.jwt}'}
    )
    response_json: dict = response.get_json()
    case.assertEqual(response.status_code, 201, msg=f'Error creating user: {response_json.get("error")}')

    return random_username


def destroy_test_user(case: TestCase, username: str) -> None:
    """
    Destroy the temporary user which was used for tests.
    :param case: Unittest test case from which to make assertions and access variables.
    :param username: Username for the temporary user to delete.
    """
    response: Response = case.client.delete(
        f'/v2/users/soft/{username}',
        headers={'Authorization': f'Bearer {case.jwts.get(username)}'}
    )
    case.assertEqual(response.status_code, 204)


def create_andy2_test_user(case: TestCase) -> None:
    """
    Create the 'andy2' test user if it does not already exist.
    :param case: Unittest test case from which to make assertions and access variables.
    """
    response: Response = case.client.get(
        '/v2/users/andy2',
        headers={'Authorization': f'Bearer {case.jwt}'}
    )

    if response.status_code != 200:
        request_body = json.dumps({'group_id': 1, 'email': 'andrew@jarombek.com'})
        response: Response = case.client.post(
            '/v2/activation_code/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {case.jwt}'}
        )

        response_json: dict = response.get_json()
        case.assertEqual(response.status_code, 200)

        activation_code_json = response_json.get('activation_code')
        activation_code = activation_code_json.get('activation_code')

        case.client.delete('/v2/users/andy2', headers={'Authorization': f'Bearer {case.jwt}'})

        request_body = json.dumps({
            "username": "andy2",
            "email": "andrew@jarombek.com",
            "first": "Andrew",
            "last": "Jarombek",
            "password": "B0unDTw0",
            "description": "",
            "member_since": str(datetime.fromisoformat('2019-12-13')),
            "activation_code": activation_code,
            "last_signin": str(datetime.fromisoformat('2019-12-14'))
        })

        response: Response = case.client.post(
            '/v2/users/',
            data=request_body,
            content_type='application/json',
            headers={'Authorization': f'Bearer {case.jwt}'}
        )
        case.assertEqual(201, response.status_code)
