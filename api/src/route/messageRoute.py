"""
Message routes in the SaintsXCTF API.  Used for retrieving, adding, updating, and deleting group messages.
Author: Andrew Jarombek
Date: 7/18/2019
"""

from flask import Blueprint, request, jsonify, Response, redirect, url_for
from dao.messageDao import MessageDao
from model.Message import Message

message_route = Blueprint('message_route', __name__, url_prefix='/v2/messages')


@message_route.route('', methods=['GET', 'POST'])
def messages_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'messages' to the message routes.
    :return: Response object letting the caller know where to redirect the request to.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages '''
        return redirect(url_for('message_route.messages'), code=302)

    elif request.method == 'POST':
        ''' [POST] /v2/messages '''
        return redirect(url_for('message_route.messages'), code=307)


@message_route.route('/', methods=['GET', 'POST'])
def messages() -> Response:
    """
    Endpoints for retrieving all the group messages and creating new messages.
    :return: JSON representation of group messages and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages/ '''
        return messages_get()

    elif request.method == 'POST':
        ''' [POST] /v2/messages/ '''
        return message_post()


@message_route.route('/<message_id>', methods=['GET', 'PUT', 'DELETE'])
def messages_with_id(message_id) -> Response:
    """
    Endpoints for retrieving a single message, editing an existing message, and deleting a message.
    :param message_id: Unique identifier for a message.
    :return: JSON representation of a group message and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages/<message_id> '''
        return message_by_id_get(message_id)

    elif request.method == 'PUT':
        ''' [PUT] /v2/messages/<message_id> '''
        return messages_by_id_put(message_id)

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/messages/<message_id> '''
        return message_by_id_delete(message_id)


@message_route.route('/soft/<message_id>', methods=['DELETE'])
def message_soft_with_id(message_id) -> Response:
    """
    Endpoints for soft deleting team/group messages.
    :param message_id: Unique identifier for a message.
    :return: JSON representation of messages and relevant metadata.
    """
    if request.method == 'DELETE':
        ''' [DELETE] /v2/messages/soft/<code> '''
        return message_by_id_soft_delete(message_id)


@message_route.route('/links', methods=['GET'])
def log_links() -> Response:
    """
    Endpoint for information about the message API endpoints.
    :return: Metadata about the message API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/messages/links '''
        return message_links_get()


def messages_get() -> Response:
    messages = MessageDao.get_messages()

    if messages is None:
        response = jsonify({
            'self': '/v2/messages',
            'messages': None,
            'error': 'an unexpected error occurred retrieving messages'
        })
        response.status_code = 500
        return response
    else:
        response = jsonify({
            'self': '/v2/messages',
            'messages': messages
        })
        response.status_code = 200
        return response


def message_post() -> Response:
    message_data: dict = request.get_json()
    message_to_add = Message(message_data)
    message_added_successfully = MessageDao.add_message(new_message=message_to_add)

    if message_added_successfully:
        message_added = MessageDao.get_message_by_id(message_id=message_to_add.message_id)

        response = jsonify({
            'self': '/v2/messages',
            'added': True,
            'message': message_added
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': '/v2/messages',
            'added': False,
            'message': None,
            'error': 'failed to create a new message'
        })
        response.status_code = 500
        return response


def message_by_id_get(message_id) -> Response:
    message = MessageDao.get_message_by_id(message_id)

    if message is None:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'log': message
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'log': None,
            'error': 'failed to retrieve a message with this id'
        })
        response.status_code = 500
        return response


def messages_by_id_put(message_id) -> Response:
    old_message = MessageDao.get_message_by_id(message_id=message_id)

    if old_message is None:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'updated': False,
            'message': None,
            'error': 'there is no existing message with this id'
        })
        response.status_code = 400
        return response

    message_data: dict = request.get_json()
    new_message = Message(message_data)

    if old_message != new_message:
        is_updated = MessageDao.update_message(new_message)

        if is_updated:
            updated_log = MessageDao.get_message_by_id(message_id=new_message.message_id)

            response = jsonify({
                'self': f'/v2/messages/{message_id}',
                'updated': True,
                'message': updated_log
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/messages/{message_id}',
                'updated': False,
                'message': None,
                'error': 'the message failed to update'
            })
            response.status_code = 500
            return response

    else:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'updated': False,
            'message': None,
            'error': 'the message submitted is equal to the existing message with the same id'
        })
        response.status_code = 400
        return response


def message_by_id_delete(message_id) -> Response:
    is_deleted = MessageDao.delete_message_by_id(message_id=message_id)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/messages/{message_id}',
            'deleted': False,
            'error': 'failed to delete the message'
        })
        response.status_code = 500
        return response


def message_by_id_soft_delete(message_id) -> Response:
    pass


def message_links_get() -> Response:
    """
    Get all the other message API endpoints.
    :return: A response object for the GET API request
    """
    response = jsonify({
        'self': f'/v2/messages/links',
        'endpoints': [
            {
                'link': '/v2/messages',
                'verb': 'GET',
                'description': 'Get all the team/group messages in the database.'
            },
            {
                'link': '/v2/messages',
                'verb': 'POST',
                'description': 'Create a new team/group message.'
            },
            {
                'link': '/v2/messages/<message_id>',
                'verb': 'GET',
                'description': 'Retrieve a single team/group message with a given unique id.'
            },
            {
                'link': '/v2/messages/<message_id>',
                'verb': 'PUT',
                'description': 'Update a team/group message with a given unique id.'
            },
            {
                'link': '/v2/messages/<message_id>',
                'verb': 'DELETE',
                'description': 'Delete a single team/group message with a given unique id.'
            },
            {
                'link': '/v2/messages/soft/<message_id>',
                'verb': 'DELETE',
                'description': 'Soft delete a single team/group message with a given unique id.'
            }
        ],
    })
    response.status_code = 200
    return response
