"""
Common code for the Notification routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/notifications/links',
    'endpoints': [
        {
            'link': '/v2/notifications',
            'verb': 'GET',
            'description': 'Get all the user notifications in the database.'
        },
        {
            'link': '/v2/notifications',
            'verb': 'POST',
            'description': 'Create a new user notification.'
        },
        {
            'link': '/v2/notifications/<notification_id>',
            'verb': 'GET',
            'description': 'Retrieve a single user notification with a given unique id.'
        },
        {
            'link': '/v2/notifications/<notification_id>',
            'verb': 'PUT',
            'description': 'Update a user notification with a given unique id.'
        },
        {
            'link': '/v2/notifications/<notification_id>',
            'verb': 'DELETE',
            'description': 'Delete a user notification with a given unique id.'
        },
        {
            'link': '/v2/notifications/soft/<notification_id>',
            'verb': 'DELETE',
            'description': 'Soft delete a user notification with a given unique id.'
        }
    ],
}
