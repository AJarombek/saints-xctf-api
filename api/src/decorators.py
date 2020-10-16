"""
Decorators used on routes throughout the application.
Support, kindness, and love are always here for you.
Author: Andrew Jarombek
Date: 10/7/2020
"""

import functools
import asyncio

import aiohttp
from flask import abort, current_app, request


def auth_required():
    """
    Make a custom decorator for endpoints, indicating that authentication is required.
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401)

            authorization_header: str = request.headers['Authorization']
            token = authorization_header.replace('Bearer ', '')

            async def authenticate():
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url=f"{current_app.config['AUTH_URL']}/authenticate",
                        json={'token': token}
                    ) as response:
                        response_body = await response.json()
                        if not response_body.get('result'):
                            current_app.logger.info('User Unauthorized')
                            abort(403)
                        else:
                            current_app.logger.info('User Authorized')

            loop = asyncio.get_event_loop()
            loop.run_until_complete(authenticate())

            return f(*args, **kwargs)
        return decorated_function
    return decorator
