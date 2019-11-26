"""
MessageFeed routes in the SaintsXCTF API.  Used for retrieving multiple messages posted in groups.
Author: Andrew Jarombek
Date: 7/27/2019
"""

from flask import Blueprint, request, jsonify, Response
from sqlalchemy.engine import ResultProxy
from dao.messageDao import MessageDao

message_feed_route = Blueprint('message_feed_route', __name__, url_prefix='/v2/message_feed')


@message_feed_route.route('/<filter_by>/<bucket>/<limit>/<offset>', methods=['GET'])
def message_feed(filter_by, bucket, limit, offset):
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
        return message_feed_get(filter_by, bucket, limit, offset)


@message_feed_route.route('/links', methods=['GET'])
def message_feed_links() -> Response:
    """
    Endpoint for information about the message feed API endpoints.
    :return: Metadata about the message feed API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/message_feed/links '''
        return message_feed_links_get()


def message_feed_get(filter_by, bucket, limit, offset):
    """
    Get a list of messages based on certain filters.
    :param filter_by: The filtering mechanism for the messages.  You can filter by group (group_name).
    :param bucket: The bucket to filter by (the group name)
    :param limit: The maximum number of messages to return
    :param offset: The number of messages to skip from the result of this filter before returning
    :return: A response object for the GET API request.
    """
    limit = int(limit)
    offset = int(offset)

    if filter_by == 'group' or filter_by == 'groups' or filter_by == 'groupname':
        messages: ResultProxy = MessageDao.get_message_feed(group_name=bucket, limit=limit, offset=offset)
    else:
        messages = None

    # Generate MessageFeed API URLs
    self_url = f'/v2/message_feed/{filter_by}/{bucket}/{limit}/{offset}'

    prev_offset = offset - limit
    if prev_offset >= 0:
        prev_url = f'/v2/message_feed/{filter_by}/{bucket}/{limit}/{prev_offset}'
    else:
        prev_url = None

    if messages is None or messages.rowcount == 0:
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
        message_list = []
        for message in messages:
            message_list.append({
                'message_id': message.message_id,
                'username': message.username,
                'first': message.first,
                'last': message.last,
                'group_name': message.group_name,
                'time': str(message.time),
                'content': message.content,
                'deleted': message.deleted
            })

        next_url = f'/v2/message_feed/{filter_by}/{bucket}/{limit}/{offset + limit}'

        response = jsonify({
            'self': self_url,
            'next': next_url,
            'prev': prev_url,
            'messages': message_list
        })
        response.status_code = 200
        return response


def message_feed_links_get() -> Response:
    """
    Get all the other message feed API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/message_feed/links',
        'endpoints': [
            {
                'link': '/v2/message_feed/<filter_by>/<bucket>/<limit>/<offset>',
                'verb': 'GET',
                'description': 'Get a list of group/team messages based on certain filters.'
            }
        ]
    })
    response.status_code = 200
    return response
