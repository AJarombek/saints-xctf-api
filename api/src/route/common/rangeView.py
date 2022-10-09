"""
Common code for the RangeView routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def range_view_links(version: str) -> Dict[str, Any]:
    """
    Get all the range view API endpoints.
    :return: A dictionary describing all range view API endpoints.
    """
    return {
        "self": f"/{version}/range_view/links",
        "endpoints": [
            {
                "link": f"/{version}/range_view/<filter_by>/<bucket>/<exercise_types>/<start>/<end>",
                "verb": "GET",
                "description": "Get a list of range view objects based on certain filters.",
            }
        ],
    }
