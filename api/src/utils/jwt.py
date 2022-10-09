"""
Helper functions for working with the JWT passed to the API for authentication.
Author: Andrew Jarombek
Date: 3/8/2021
"""

import base64
import json

from flask import Request


def get_claims(request: Request) -> dict:
    """
    Get the claims from a JWT payload.
    :param request: An object with details about the HTTP request.
    """
    authorization_header: str = request.headers.get("Authorization")
    token = authorization_header.replace("Bearer ", "")
    jwt_claims = base64.b64decode(token.split(".")[1] + "==")
    return json.loads(jwt_claims)
