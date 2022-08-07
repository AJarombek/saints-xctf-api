"""
Common code for flair routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/5/2022
"""

links = {
    'self': f'/v2/flair/links',
    'endpoints': [
        {
            'link': '/v2/flair',
            'verb': 'POST',
            'description': 'Create a new flair item.'
        }
    ],
}
