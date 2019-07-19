"""
Message routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting group messages.
Author: Andrew Jarombek
Date: 7/18/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.messageDao import MessageDao
from model.Message import Message

message_route = Blueprint('message_route', __name__, url_prefix='/v2/messages')


@message_route.route('/', methods=['GET', 'POST'])
def messages():
    """
    Endpoints for retrieving all the group messages and creating new messages.
    :return: JSON representation of group messages and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages '''
        messages = MessageDao.get_messages()

    elif request.method == 'POST':
        ''' [POST] /v2/messages '''
        pass


@message_route.route('/<message_id>', methods=['GET', 'PUT', 'DELETE'])
def logs_with_id(message_id):
    """
    Endpoints for retrieving a single message, editing an existing message, and deleting a message.
    :param message_id: Unique identifier for a message.
    :return: JSON representation of a group message and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages/<message_id> '''
        pass

    elif request.method == 'PUT':
        ''' [PUT] /v2/messages/<message_id> '''
        pass

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/messages/<message_id> '''
        pass
