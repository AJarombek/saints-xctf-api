"""
Common code for the User routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/users/links',
    'endpoints': [
        {
            'link': '/v2/users',
            'verb': 'GET',
            'description': 'Get all the users in the database.'
        },
        {
            'link': '/v2/users',
            'verb': 'POST',
            'description': 'Create a new user.'
        },
        {
            'link': '/v2/users/<username>',
            'verb': 'GET',
            'description': 'Retrieve a single user with a given username.'
        },
        {
            'link': '/v2/users/<username>',
            'verb': 'PUT',
            'description': 'Update a user with a given username.'
        },
        {
            'link': '/v2/users/<username>',
            'verb': 'DELETE',
            'description': 'Delete a user with a given username.'
        },
        {
            'link': '/v2/users/soft/<username>',
            'verb': 'DELETE',
            'description': 'Soft delete a user with a given username.'
        },
        {
            'link': '/v2/users/snapshot/<username>',
            'verb': 'GET',
            'description': 'Get a snapshot about a user and their exercise statistics with a given username.'
        },
        {
            'link': '/v2/users/groups/<username>',
            'verb': 'GET',
            'description': 'Get a list of groups that a user with a given username is a member of.'
        },
        {
            'link': '/v2/users/teams/<username>',
            'verb': 'GET',
            'description': 'Get a list of teams that a user with a given username is a member of.'
        },
        {
            'link': '/v2/users/memberships/<username>',
            'verb': 'GET',
            'description': 'Get a list of teams with nested lists of groups that a user is a member of.'
        },
        {
            'link': '/v2/users/memberships/<username>',
            'verb': 'PUT',
            'description': "Update a user's group and team memberships."
        },
        {
            'link': '/v2/users/notifications/<username>',
            'verb': 'GET',
            'description': 'Get a list of notifications for a user with a given username.'
        },
        {
            'link': '/v2/users/flair/<username>',
            'verb': 'GET',
            'description': 'Get a list of flair objects assigned to a user with a given username.'
        },
        {
            'link': '/v2/users/statistics/<username>',
            'verb': 'GET',
            'description': 'Get exercise statistics for a user with a given username.'
        },
        {
            'link': '/v2/users/<username>/change_password',
            'verb': 'PUT',
            'description': 'Update a user with a given username.  Specifically, alter the users password.'
        },
        {
            'link': '/v2/users/<username>/update_last_login',
            'verb': 'PUT',
            'description': 'Update a user with a given username.  Specifically, change the users last login date.'
        },
        {
            'link': '/v2/users/lookup/<username>',
            'verb': 'GET',
            'description': 'Check if a user exists with a username or email.'
        }
    ],
}
