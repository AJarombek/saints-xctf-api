"""
Common code for comment routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

links = {
    'self': f'/v2/comments/links',
    'endpoints': [
        {
            'link': '/v2/comments',
            'verb': 'GET',
            'description': 'Get all the comments in the database.'
        },
        {
            'link': '/v2/comments',
            'verb': 'POST',
            'description': 'Create a new comment.'
        },
        {
            'link': '/v2/comments/<comment_id>',
            'verb': 'GET',
            'description': 'Retrieve a single comment with a given unique id.'
        },
        {
            'link': '/v2/comments/<comment_id>',
            'verb': 'PUT',
            'description': 'Update a comment with a given unique id.'
        },
        {
            'link': '/v2/comments/<comment_id>',
            'verb': 'DELETE',
            'description': 'Delete a single comment with a given unique id.'
        },
        {
            'link': '/v2/comments/soft/<comment_id>',
            'verb': 'DELETE',
            'description': 'Soft delete a single comment with a given unique id.'
        }
    ],
}
