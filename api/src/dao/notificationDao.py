"""
Notification data access from the SaintsXCTF MySQL database.  Contains notifications for events users
should be aware of.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from sqlalchemy.engine import ResultProxy
from dao.basicDao import BasicDao
from model.Notification import Notification


class NotificationDao:

    @staticmethod
    def get_notifications() -> list:
        """
        Retrieve all the notifications in the database.
        :return: The result of the query.
        """
        return Notification.query\
            .order_by(Notification.time)\
            .filter(Notification.deleted.is_(False))\
            .all()

    @staticmethod
    def get_notification_by_id(notification_id: int) -> Notification:
        """
        Retrieve a single notification by its unique id
        :param notification_id: The unique identifier for a notification.
        :return: The result of the query.
        """
        return Notification.query\
            .filter_by(notification_id=notification_id)\
            .filter(Notification.deleted.is_(False))\
            .first()

    @staticmethod
    def get_notification_by_username(username: str) -> ResultProxy:
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
            AND deleted IS FALSE
            ORDER BY time DESC
            ''',
            {'username': username}
        )

    @staticmethod
    def add_notification(new_notification: Notification) -> bool:
        """
        Add a notification for a user to the database.
        :param new_notification: Object representing a notification for a user.
        :return: True if the notification is inserted into the database, False otherwise.
        """
        db.session.add(new_notification)
        return BasicDao.safe_commit()

    @staticmethod
    def update_notification(notification: Notification) -> bool:
        """
        Update a notification in the database. Certain fields (notification_id, username, time, link, description)
        can't be modified.
        :param notification: Object representing an updated notification.
        :return: True if the notification is updated in the database, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE notifications 
            SET viewed=:viewed
            WHERE notification_id=:notification_id
            AND deleted IS FALSE
            ''',
            {
                'notification_id': notification.notification_id,
                'viewed': notification.viewed
            }
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_notification_by_id(notification_id: int) -> bool:
        """
        Delete a notification from the database based on its id.
        :param notification_id: ID which uniquely identifies the notification.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM notifications WHERE notification_id=:notification_id AND deleted IS FALSE',
            {'notification_id': notification_id}
        )
        return BasicDao.safe_commit()

    @staticmethod
    def soft_delete_notification(notification: Notification) -> bool:
        """
        Soft Delete a user notification from the database.
        :param notification: Object representing a notification to soft delete.
        :return: True if the soft deletion was successful without error, False otherwise.
        """
        db.session.execute(
            '''
            UPDATE notifications SET 
                deleted=:deleted,
                modified_date=:modified_date,
                modified_app=:modified_app,
                deleted_date=:deleted_date,
                deleted_app=:deleted_app
            WHERE notification_id=:notification_id
            AND deleted IS FALSE
            ''',
            {
                'notification_id': notification.notification_id,
                'deleted': notification.deleted,
                'modified_date': notification.modified_date,
                'modified_app': notification.modified_app,
                'deleted_date': notification.deleted_date,
                'deleted_app': notification.deleted_app
            }
        )
        return BasicDao.safe_commit()
