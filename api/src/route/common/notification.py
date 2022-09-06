"""
Common code for the Notification routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def notification_links(version: str) -> Dict[str, Any]:
    """
    Get all the notification API endpoints.
    :return: A dictionary describing all notification API endpoints.
    """
    return {
        'self': f'/{version}/notifications/links',
        'endpoints': [
            {
                'link': f'/{version}/notifications',
                'verb': 'GET',
                'description': 'Get all the user notifications in the database.'
            },
            {
                'link': f'/{version}/notifications',
                'verb': 'POST',
                'description': 'Create a new user notification.'
            },
            {
                'link': f'/{version}/notifications/<notification_id>',
                'verb': 'GET',
                'description': 'Retrieve a single user notification with a given unique id.'
            },
            {
                'link': f'/{version}/notifications/<notification_id>',
                'verb': 'PUT',
                'description': 'Update a user notification with a given unique id.'
            },
            {
                'link': f'/{version}/notifications/<notification_id>',
                'verb': 'DELETE',
                'description': 'Delete a user notification with a given unique id.'
            },
            {
                'link': f'/{version}/notifications/soft/<notification_id>',
                'verb': 'DELETE',
                'description': 'Soft delete a user notification with a given unique id.'
            }
        ],
    }
