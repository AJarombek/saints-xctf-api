"""
Common code for the RangeView routes in the SaintsXCTF API.
Author: Andrew Jarombek
Date: 8/6/2022
"""

links = {
    'self': f'/v2/range_view/links',
    'endpoints': [
        {
            'link': '/v2/range_view/<filter_by>/<bucket>/<exercise_types>/<start>/<end>',
            'verb': 'GET',
            'description': 'Get a list of range view objects based on certain filters.'
        }
    ]
}
