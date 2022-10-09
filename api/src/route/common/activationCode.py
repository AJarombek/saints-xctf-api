"""
Common code for activation code routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

from typing import Dict, Any


def activation_code_links(version: str) -> Dict[str, Any]:
    """
    Get all the activation code API endpoints.
    :return: A dictionary describing all activation code API endpoints.
    """
    return {
        "self": f"/{version}/activation_code/links",
        "endpoints": [
            {
                "link": f"/{version}/activation_code",
                "verb": "POST",
                "description": "Create a new activation code.",
            },
            {
                "link": f"/{version}/activation_code/<code>",
                "verb": "GET",
                "description": "Retrieve a single activation code with a given unique code.",
            },
            {
                "link": f"/{version}/activation_code/<code>",
                "verb": "DELETE",
                "description": "Delete a single activation code.",
            },
            {
                "link": f"/{version}/activation_code/soft/<code>",
                "verb": "DELETE",
                "description": "Soft delete a single activation code.",
            },
        ],
    }
