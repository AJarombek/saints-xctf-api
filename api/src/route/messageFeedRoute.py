"""
MessageFeed routes in the SaintsXCTF API.  Used for retrieving multiple messages posted in groups.
Author: Andrew Jarombek
Date: 7/27/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.messageDao import MessageDao

message_feed_route = Blueprint('message_feed_route', __name__, url_prefix='/v2/messagefeed')


@message_feed_route.route('/<filter_by>/<bucket>/<limit>/<offset>', methods=['GET'])
def messages(filter_by, bucket, limit, offset):
    """
    Endpoints for retrieving group messages based on filters.
    :param filter_by: The filtering mechanism for the messages.  You can filter by group (group_name).
    :param bucket: The bucket to filter by (the group name)
    :param limit: The maximum number of messages to return
    :param offset: The number of messages to skip from the result of this filter before returning
    :return: JSON representation of group messages and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/message_feed '''
        if filter_by == 'group' or filter_by == 'groups':
            messages = MessageDao.get_message_feed(group_name=bucket, limit=limit, offset=offset)
        else:
            messages = None

        # Generate MessageFeed API URLs
        self_url = f'/v2/messagefeed/{filter_by}/{bucket}/{limit}/{offset}'

        prev_offset = (offset - limit) >= 0
        if prev_offset:
            prev_url = f'/v2/messagefeed/{filter_by}/{bucket}/{limit}/{prev_offset}'
        else:
            prev_url = None

        if messages is None:
            next_url = None

            response = jsonify({
                'self': self_url,
                'next': next_url,
                'prev': prev_url,
                'messages': None,
                'error': 'no messages found in this feed'
            })
            response.status_code = 500
            return response
        else:
            next_url = f'/v2/messagefeed/{filter_by}/{bucket}/{limit}/{offset + limit}'

            response = jsonify({
                'self': self_url,
                'next': next_url,
                'prev': prev_url,
                'messages': messages
            })
            response.status_code = 200
            return response
