"""
Notification ORM model for the 'notification' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Notification(db.Model):
    def __init__(self, notification: dict):
        """
        Initialize a Notification by passing in a dictionary.
        :param notification: A dictionary with fields matching the Notification fields
        """
        self.notification_id = notification.get("notification_id")
        self.username = notification.get("username")
        self.time = notification.get("time")
        self.link = notification.get("link")
        self.viewed = notification.get("viewed")
        self.description = notification.get("description")
        self.deleted = notification.get("deleted")
        self.created_date = notification.get("created_date")
        self.created_user = notification.get("created_user")
        self.created_app = notification.get("created_app")
        self.modified_date = notification.get("modified_date")
        self.modified_user = notification.get("modified_user")
        self.modified_app = notification.get("modified_app")
        self.deleted_date = notification.get("deleted_date")
        self.deleted_user = notification.get("deleted_user")
        self.deleted_app = notification.get("deleted_app")

    __tablename__ = "notifications"
    __bind_key__ = "app"

    # Data Columns
    notification_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(
        db.VARCHAR(20), db.ForeignKey("users.username"), nullable=False, index=True
    )
    time = Column(db.DATETIME, nullable=False, index=True)
    link = Column(db.VARCHAR(127))
    viewed = Column(db.CHAR(1), nullable=False)
    description = Column(db.VARCHAR(127))
    deleted = Column(db.BOOLEAN)

    # Audit Columns
    created_date = Column(db.DATETIME)
    created_user = Column(db.VARCHAR(31))
    created_app = Column(db.VARCHAR(31))
    modified_date = Column(db.DATETIME)
    modified_user = Column(db.VARCHAR(31))
    modified_app = Column(db.VARCHAR(31))
    deleted_date = Column(db.DATETIME)
    deleted_user = Column(db.VARCHAR(31))
    deleted_app = Column(db.VARCHAR(31))

    def __str__(self):
        """
        String representation of a notification for a user.  This representation is meant to be human readable.
        :return: The notification in string form.
        """
        return (
            f"Notification: [notification_id: {self.notification_id}, username: {self.username}, "
            f"time: {self.time}, link: {self.link}, viewed: {self.viewed}, description: {self.description}, "
            f"deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a notification for a user.  This representation is meant to be machine readable.
        :return: The notification in string form.
        """
        return "<Notification %d>" % self.notification_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this notification for a user.
        :return: True if the objects are equal, False otherwise.
        """
        return Notification.compare(self, other)

    @classmethod
    def compare(cls, notification_1, notification_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be notifications.
        :param notification_1: The first notification object.
        :param notification_2: The second notification object.
        :return: True if the objects are equal, False otherwise.
        """
        return all(
            [
                notification_1.notification_id == notification_2.notification_id,
                notification_1.username == notification_2.username,
                str(notification_1.time) == str(notification_2.time),
                notification_1.link == notification_2.link,
                notification_1.viewed == notification_2.viewed,
                notification_1.description == notification_2.description,
                notification_1.deleted == notification_2.deleted,
            ]
        )
