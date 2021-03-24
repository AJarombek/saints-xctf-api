"""
Blueprint for a Flask test suite which is extended by other test suites
Author: Andrew Jarombek
Date: 6/22/2019
"""

import unittest
import os
import asyncio
import json

import boto3
import aiohttp
from flask.testing import FlaskClient

from config import config
from app import create_app
from database import db


class TestSuite(unittest.TestCase):
    jwt = None
    auth_url = None

    @classmethod
    def setUpClass(cls) -> None:
        flask_env = os.getenv('FLASK_ENV') or 'local'
        auth_url = config[flask_env].AUTH_URL
        TestSuite.auth_url = auth_url

        secretsmanager = boto3.client('secretsmanager')
        response = secretsmanager.get_secret_value(SecretId=f'saints-xctf-andy-password')
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        client_secret = secret_dict.get("password")

        async def token():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=f"{auth_url}/token",
                    json={'clientId': 'andy', 'clientSecret': client_secret}
                ) as response:
                    response_body = await response.json()
                    result = response_body.get('result')
                    if result:
                        TestSuite.jwt = result

        asyncio.run(token())

    def setUp(self) -> None:
        """
        Set up logic for the test suite.  Invoked before unit tests are run.
        """
        if os.environ.get('ENV') == 'localtest':
            env = 'localtest'
        else:
            env = 'test'

        self.app = create_app(env)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client: FlaskClient = self.app.test_client()
        self.jwt = TestSuite.jwt
        self.auth_url = TestSuite.auth_url

    def tearDown(self) -> None:
        """
        Tear down logic for the test suite.  Invoked after unit tests are run.
        """
        db.session.remove()
        self.app_context.pop()
