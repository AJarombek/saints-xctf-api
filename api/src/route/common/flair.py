"""
Common code for flair routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

from typing import Dict, Any


def flair_links(version: str) -> Dict[str, Any]:
    """
    Get all the flair API endpoints.
    :return: A dictionary describing all flair API endpoints.
    """
    return {
        "self": f"/{version}/flair/links",
        "endpoints": [
            {
                "link": f"/{version}/flair",
                "verb": "POST",
                "description": "Create a new flair item.",
            }
        ],
    }
