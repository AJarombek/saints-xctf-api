"""
Notification routes in the SaintsXCTF API.  Used for retrieving, creating, updating and deleting notifications for
comments on logs, references, group member requests, and group messages.
Author: Andrew Jarombek
Date: 8/6/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.notificationDao import NotificationDao

notification_route = Blueprint('notification_route', __name__, url_prefix='/v2/notification')


@notification_route.route('/', methods=['GET', 'POST'])
def notifications():
    if request.method == 'GET':
        ''' [GET] /v2/notification '''
        pass
    elif request.method == 'POST':
        ''' [POST] /v2/notification '''
        pass


@notification_route.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def notification_by_id(id):
    if request.method == 'GET':
        ''' [GET] /v2/notification/<id> '''
        pass
    elif request.method == 'PUT':
        ''' [PUT] /v2/notification/<id> '''
        pass
    elif request.method == 'DELETE':
        ''' [DELETE] /v2/notification/<id> '''
        pass
