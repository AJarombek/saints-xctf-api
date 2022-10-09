"""
Common code for the ForgotPassword routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def forgot_password_links(version: str) -> Dict[str, Any]:
    """
    Get all the forgot password API endpoints.
    :return: A dictionary describing all forgot password API endpoints.
    """
    return {
        "self": f"/{version}/forgot_password/links",
        "endpoints": [
            {
                "link": f"/{version}/forgot_password/<username>",
                "verb": "GET",
                "description": "Retrieve a single forgot password code assigned to a given username.",
            },
            {
                "link": f"/{version}/forgot_password/<username>",
                "verb": "POST",
                "description": "Create a new forgot password code.",
            },
            {
                "link": f"/{version}/forgot_password/validate/<code>",
                "verb": "GET",
                "description": "Validate if a forgot password code exists.",
            },
        ],
    }
