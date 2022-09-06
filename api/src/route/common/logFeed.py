"""
Common code for the LogFeed routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def log_feed_links(version: str) -> Dict[str, Any]:
    """
    Get all the log feed API endpoints.
    :return: A dictionary describing all log feed API endpoints.
    """
    return {
        'self': f'/{version}/log_feed/links',
        'endpoints': [
            {
                'link': f'/{version}/log_feed/<filter_by>/<bucket>/<limit>/<offset>',
                'verb': 'GET',
                'description': 'Get a list of exercise logs based on certain filters.'
            }
        ]
    }
