"""
Common code for activation code routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

links = {
    'self': f'/v2/activation_code/links',
    'endpoints': [
        {
            'link': '/v2/activation_code',
            'verb': 'POST',
            'description': 'Create a new activation code.'
        },
        {
            'link': '/v2/activation_code/<code>',
            'verb': 'GET',
            'description': 'Retrieve a single activation code with a given unique code.'
        },
        {
            'link': '/v2/activation_code/<code>',
            'verb': 'DELETE',
            'description': 'Delete a single activation code.'
        },
        {
            'link': '/v2/activation_code/soft/<code>',
            'verb': 'DELETE',
            'description': 'Soft delete a single activation code.'
        }
    ],
}
