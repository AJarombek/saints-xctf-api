"""
Common code for the ForgotPassword routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/forgot_password/links',
    'endpoints': [
        {
            'link': '/v2/forgot_password/<username>',
            'verb': 'GET',
            'description': 'Retrieve a single forgot password code assigned to a given username.'
        },
        {
            'link': '/v2/forgot_password/<username>',
            'verb': 'POST',
            'description': 'Create a new forgot password code.'
        },
        {
            'link': '/v2/forgot_password/validate/<code>',
            'verb': 'GET',
            'description': 'Validate if a forgot password code exists.'
        }
    ],
}