"""
Common code for comment routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

from typing import Dict, Any


def comment_links(version: str) -> Dict[str, Any]:
    """
    Get all the comment API endpoints.
    :return: A dictionary describing all comment API endpoints.
    """
    return {
        'self': f'/{version}/comments/links',
        'endpoints': [
            {
                'link': f'/{version}/comments',
                'verb': 'GET',
                'description': 'Get all the comments in the database.'
            },
            {
                'link': f'/{version}/comments',
                'verb': 'POST',
                'description': 'Create a new comment.'
            },
            {
                'link': f'/{version}/comments/<comment_id>',
                'verb': 'GET',
                'description': 'Retrieve a single comment with a given unique id.'
            },
            {
                'link': f'/{version}/comments/<comment_id>',
                'verb': 'PUT',
                'description': 'Update a comment with a given unique id.'
            },
            {
                'link': f'/{version}/comments/<comment_id>',
                'verb': 'DELETE',
                'description': 'Delete a single comment with a given unique id.'
            },
            {
                'link': f'/{version}/comments/soft/<comment_id>',
                'verb': 'DELETE',
                'description': 'Soft delete a single comment with a given unique id.'
            }
        ],
    }
