"""
Common code for the Log routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/logs/links',
    'endpoints': [
        {
            'link': '/v2/logs',
            'verb': 'GET',
            'description': 'Get all the exercise logs in the database.'
        },
        {
            'link': '/v2/logs',
            'verb': 'POST',
            'description': 'Create a new exercise log.'
        },
        {
            'link': '/v2/logs/<log_id>',
            'verb': 'GET',
            'description': 'Retrieve a single exercise log with a given unique id.'
        },
        {
            'link': '/v2/logs/<log_id>',
            'verb': 'PUT',
            'description': 'Update an exercise log with a given unique id.'
        },
        {
            'link': '/v2/logs/<log_id>',
            'verb': 'DELETE',
            'description': 'Delete a single exercise log with a given unique id.'
        },
        {
            'link': '/v2/logs/soft/<comment_id>',
            'verb': 'DELETE',
            'description': 'Soft delete a single exercise log with a given unique id.'
        }
    ],
}
