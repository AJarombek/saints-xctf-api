"""
Notification model that only includes data columns.
Author: Andrew Jarombek
Date: 11/30/2019
"""

from .Notification import Notification


class NotificationData:
    def __init__(self, notification: Notification):
        """
        Create a notification object without any auditing fields.
        :param notification: The original Notification object with auditing fields.
        """
        if notification is not None:
            self.notification_id = notification.notification_id
            self.username = notification.username
            self.time = notification.time
            self.link = notification.link
            self.viewed = notification.viewed
            self.description = notification.description
            self.deleted = notification.deleted

    def __str__(self):
        """
        String representation of a notification for a user.  This representation is meant to be human readable.
        :return: The notification in string form.
        """
        return f'NotificationData: [notification_id: {self.notification_id}, username: {self.username}, ' \
            f'time: {self.time}, link: {self.link}, viewed: {self.viewed}, description: {self.description}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a notification for a user.  This representation is meant to be machine readable.
        :return: The notification in string form.
        """
        return '<NotificationData %d>' % self.notification_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this notification for a user.
        :return: True if the objects are equal, False otherwise.
        """
        return Notification.compare(self, other)
