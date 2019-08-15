"""
Notification routes in the SaintsXCTF API.  Used for retrieving, creating, updating and deleting notifications for
comments on logs, references, group member requests, and group messages.
Author: Andrew Jarombek
Date: 8/6/2019
"""

from flask import Blueprint, request, jsonify, current_app
from model.Notification import Notification
from dao.notificationDao import NotificationDao

notification_route = Blueprint('notification_route', __name__, url_prefix='/v2/notifications')


@notification_route.route('/', methods=['GET', 'POST'])
def notifications():
    """
    Endpoints for retrieving all the notifications and creating new notifications.
    :return: JSON representation of notifications and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/notifications '''
        notifications = NotificationDao.get_notifications()

        if notifications is None:
            response = jsonify({
                'self': '/v2/notifications',
                'notifications': None,
                'error': 'an unexpected error occurred retrieving notifications'
            })
            response.status_code = 500
            return response
        else:
            response = jsonify({
                'self': '/v2/notifications',
                'notifications': notifications
            })
            response.status_code = 200
            return response

    elif request.method == 'POST':
        ''' [POST] /v2/notifications '''
        notification_data: dict = request.get_json()
        notification_to_add = Notification(notification_data)
        notification_added_successfully = NotificationDao.add_notification(new_notification=notification_to_add)

        if notification_added_successfully:
            notification_added = NotificationDao.get_notification_by_id(notification_to_add.notification_id)

            response = jsonify({
                'self': '/v2/notifications',
                'added': True,
                'notification': notification_added
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': '/v2/notifications',
                'added': False,
                'notification': None,
                'error': 'failed to create a new notification'
            })
            response.status_code = 500
            return response


@notification_route.route('/<notification_id>', methods=['GET', 'PUT', 'DELETE'])
def notification_by_id(notification_id):
    """
    Endpoints for retrieving a single notification, updating existing notifications, and deleting notifications.
    :param notification_id: Unique identifier for a notification.
    :return: JSON representation of notifications and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/notifications/<notification_id> '''
        notification = NotificationDao.get_notification_by_id(notification_id=notification_id)

        if notification is None:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'notification': None,
                'error': 'there is no notification with this identifier'
            })
            response.status_code = 400
            return response
        else:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'notification': notification
            })
            response.status_code = 200
            return response

    elif request.method == 'PUT':
        ''' [PUT] /v2/notifications/<notification_id> '''
        old_notification = NotificationDao.get_notification_by_id(notification_id=notification_id)

        if old_notification is None:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'updated': False,
                'notification': None,
                'error': 'there is no existing notification with this id'
            })
            response.status_code = 400
            return response

        notification_data: dict = request.get_json()
        new_notification = Notification(notification_data)

        if old_notification != new_notification:
            is_updated = NotificationDao.update_notification(notification=new_notification)

            if is_updated:
                updated_notification = NotificationDao.get_notification_by_id(
                    notification_id=new_notification.notification_id
                )

                response = jsonify({
                    'self': f'/v2/notifications/{notification_id}',
                    'updated': True,
                    'notification': updated_notification
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({
                    'self': f'/v2/notifications/{notification_id}',
                    'updated': False,
                    'notification': None,
                    'error': 'the notification failed to update'
                })
                response.status_code = 500
                return response
        else:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'updated': False,
                'notification': None,
                'error': 'the notification submitted is equal to the existing notification with the same id'
            })
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/notifications/<notification_id> '''
        is_deleted = NotificationDao.delete_notification_by_id(notification_id=notification_id)

        if is_deleted:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'deleted': True,
            })
            response.status_code = 204
            return response
        else:
            response = jsonify({
                'self': f'/v2/notifications/{notification_id}',
                'deleted': False,
                'error': 'failed to delete the notification'
            })
            response.status_code = 500
            return response
