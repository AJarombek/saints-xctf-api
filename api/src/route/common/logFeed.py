"""
Common code for the LogFeed routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/log_feed/links',
    'endpoints': [
        {
            'link': '/v2/log_feed/<filter_by>/<bucket>/<limit>/<offset>',
            'verb': 'GET',
            'description': 'Get a list of exercise logs based on certain filters.'
        }
    ]
}
