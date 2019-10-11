"""
Global routes in the SaintsXCTF API.  Used for retrieving information about the API.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from flask import Blueprint, jsonify

api_route = Blueprint('api_route', __name__, url_prefix='/')


@api_route.route('/', methods=['GET'])
def api():
    """
    Entry point for the SaintsXCTF API
    :return: A JSON welcome message
    """
    return jsonify({
        'self_link': '/',
        'api_name': 'saints-xctf-api',
        'versions_link': '/versions'
    })


@api_route.route('/versions', methods=['GET'])
def versions():
    return jsonify({
        'self': '/versions',
        'version_latest': '/v2',
        'version_1': None,
        'version_2': '/v2'
    })


@api_route.route('/v2', methods=['GET'])
def version2():
    return jsonify({
        'self': '/v2',
        'version': 2,
        'latest': True,
        'links': '/v2/links'
    })


@api_route.route('/v2/links', methods=['GET'])
def links():
    return jsonify({
        'self': '/v2/links',
        'activation_code': '/v2/activation_code/links',
        'comment': '/v2/comments/links',
        'flair': '/v2/flair/links',
        'forgot_password': '/v2/forgot_password/links',
        'group': '/v2/groups/links',
        'log_feed': '/v2/log_feed/links',
        'log': '/v2/logs/links',
        'mail': '/v2/mail/links',
        'message_feed': '/v2/message_feed/links',
        'message': '/v2/messages/links',
        'notification': '/v2/notifications/links',
        'range_view': '/v2/range_view/links',
        'user': '/v2/users/links'
    })
