"""
Decorators used on routes throughout the application.
Support, kindness, and love are always here for you.
Author: Andrew Jarombek
Date: 10/7/2020
"""

import functools
import asyncio
from typing import List, Optional

import aiohttp
from flask import abort, current_app, request

from utils.literals import HTTPMethod

GET: HTTPMethod = "GET"
POST: HTTPMethod = "POST"
PUT: HTTPMethod = "PUT"
PATCH: HTTPMethod = "PATCH"
DELETE: HTTPMethod = "DELETE"


def auth_required(enabled_methods: Optional[List[HTTPMethod]] = None):
    """
    Make a custom decorator for endpoints, indicating that authentication is required.
    :param enabled_methods: HTTP methods (verbs) that require authentication for an endpoint.
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if enabled_methods and request.method not in enabled_methods:
                current_app.logger.info(
                    f"Authentication is skipped for {request.method} requests to {request.url}"
                )
            else:
                if "Authorization" not in request.headers:
                    abort(401)

                authorization_header: str = request.headers["Authorization"]
                token = authorization_header.replace("Bearer ", "")

                async def authenticate():
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url=f"{current_app.config['AUTH_URL']}/authenticate",
                            json={"token": token},
                        ) as response:
                            response_body = await response.json()
                            if not response_body.get("result"):
                                current_app.logger.info("User Unauthorized")
                                abort(403)
                            else:
                                current_app.logger.info("User Authorized")

                asyncio.run(authenticate())

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def disabled(disabled_methods: Optional[List[HTTPMethod]] = None):
    """
    Make a custom decorator for endpoints that are currently disabled and should not be invoked.
    :param disabled_methods: HTTP methods (verbs) that are disabled and follow the rules of this annotation.
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if disabled_methods and request.method not in disabled_methods:
                current_app.logger.info(
                    f"{request.method} requests to {request.url} are not disabled."
                )
            else:
                current_app.logger.info("This endpoint is disabled.")
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
