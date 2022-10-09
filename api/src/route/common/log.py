"""
Common code for the Log routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def log_links(version: str) -> Dict[str, Any]:
    """
    Get all the log API endpoints.
    :return: A dictionary describing all log API endpoints.
    """
    return {
        "self": f"/{version}/logs/links",
        "endpoints": [
            {
                "link": f"/{version}/logs",
                "verb": "GET",
                "description": "Get all the exercise logs in the database.",
            },
            {
                "link": f"/{version}/logs",
                "verb": "POST",
                "description": "Create a new exercise log.",
            },
            {
                "link": f"/{version}/logs/<log_id>",
                "verb": "GET",
                "description": "Retrieve a single exercise log with a given unique id.",
            },
            {
                "link": f"/{version}/logs/<log_id>",
                "verb": "PUT",
                "description": "Update an exercise log with a given unique id.",
            },
            {
                "link": f"/{version}/logs/<log_id>",
                "verb": "DELETE",
                "description": "Delete a single exercise log with a given unique id.",
            },
            {
                "link": f"/{version}/logs/soft/<comment_id>",
                "verb": "DELETE",
                "description": "Soft delete a single exercise log with a given unique id.",
            },
        ],
    }
