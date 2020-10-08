"""
Decorators used on routes throughout the application.
Support, kindness, and love are always here for you.
Author: Andrew Jarombek
Date: 10/7/2020
"""

import functools

import aiohttp
from flask import abort, current_app


def auth_required():
    """
    Make a custom decorator for endpoints, indicating that authentication is required.
    """
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(*args, **kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=f"{current_app.config['AUTH_URL']}/authenticate",
                    data={'token': ''}
                ) as response:
                    if not response:
                        print('User Unauthorized')
                        abort(403)
                    else:
                        print('User Authorized')

            return await f(*args, **kwargs)
        return decorated_function
    return decorator
