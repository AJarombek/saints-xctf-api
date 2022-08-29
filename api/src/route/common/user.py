"""
Common code for the User routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

from typing import Dict, Any


def user_links(version: str) -> Dict[str, Any]:
    """
    Get all the user API endpoints.
    :return: A dictionary describing all user API endpoints.
    """
    return {
        'self': f'/{version}/users/links',
        'endpoints': [
            {
                'link': f'/{version}/users',
                'verb': 'GET',
                'description': 'Get all the users in the database.'
            },
            {
                'link': f'/{version}/users',
                'verb': 'POST',
                'description': 'Create a new user.'
            },
            {
                'link': f'/{version}/users/<username>',
                'verb': 'GET',
                'description': 'Retrieve a single user with a given username.'
            },
            {
                'link': f'/{version}/users/<username>',
                'verb': 'PUT',
                'description': 'Update a user with a given username.'
            },
            {
                'link': f'/{version}/users/<username>',
                'verb': 'DELETE',
                'description': 'Delete a user with a given username.'
            },
            {
                'link': f'/{version}/users/soft/<username>',
                'verb': 'DELETE',
                'description': 'Soft delete a user with a given username.'
            },
            {
                'link': f'/{version}/users/snapshot/<username>',
                'verb': 'GET',
                'description': 'Get a snapshot about a user and their exercise statistics with a given username.'
            },
            {
                'link': f'/{version}/users/groups/<username>',
                'verb': 'GET',
                'description': 'Get a list of groups that a user with a given username is a member of.'
            },
            {
                'link': f'/{version}/users/teams/<username>',
                'verb': 'GET',
                'description': 'Get a list of teams that a user with a given username is a member of.'
            },
            {
                'link': f'/{version}/users/memberships/<username>',
                'verb': 'GET',
                'description': 'Get a list of teams with nested lists of groups that a user is a member of.'
            },
            {
                'link': f'/{version}/users/memberships/<username>',
                'verb': 'PUT',
                'description': "Update a user's group and team memberships."
            },
            {
                'link': f'/{version}/users/notifications/<username>',
                'verb': 'GET',
                'description': 'Get a list of notifications for a user with a given username.'
            },
            {
                'link': f'/{version}/users/flair/<username>',
                'verb': 'GET',
                'description': 'Get a list of flair objects assigned to a user with a given username.'
            },
            {
                'link': f'/{version}/users/statistics/<username>',
                'verb': 'GET',
                'description': 'Get exercise statistics for a user with a given username.'
            },
            {
                'link': f'/{version}/users/<username>/change_password',
                'verb': 'PUT',
                'description': 'Update a user with a given username.  Specifically, alter the users password.'
            },
            {
                'link': f'/{version}/users/<username>/update_last_login',
                'verb': 'PUT',
                'description': 'Update a user with a given username.  Specifically, change the users last login date.'
            },
            {
                'link': f'/{version}/users/lookup/<username>',
                'verb': 'GET',
                'description': 'Check if a user exists with a username or email.'
            }
        ],
    }
