"""
Notification data access from the SaintsXCTF MySQL database.  Contains notifications for events users
should be aware of.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from model.Notification import Notification


class NotificationDao:

    @staticmethod
    def get_notifications() -> list:
        """
        Retrieve all the notifications in the database.
        :return: The result of the query.
        """
        return Notification.query.order_by(Notification.time).all()

    @staticmethod
    def get_notification_by_id(notification_id: int) -> dict:
        """
        Retrieve a single notification by its unique id
        :param notification_id: The unique identifier for a notification.
        :return: The result of the query.
        """
        return Notification.query.filter_by(notification_id=notification_id).first()

    @staticmethod
    def get_notification_by_username(username: str) -> list:
        """
        Retrieve all the notifications for a user from the past two weeks
        :param username: Unique identifier for a user
        :return: A list of notifications
        """
        return db.session.execute(
            '''
            SELECT * FROM notifications 
            WHERE username=:username 
            AND time >= CURDATE() - INTERVAL DAYOFWEEK(CURDATE()) + 13 DAY 
            ORDER BY time DESC
            ''',
            {'username': username}
        )
