"""
Notification data access from the SaintsXCTF demo database.  Contains notifications for events users
should be aware of.
Author: Andrew Jarombek
Date: 9/14/2022
"""

from app import app
from database import db
from sqlalchemy.engine.cursor import ResultProxy


class NotificationDemoDao:
    engine = db.get_engine(app=app, bind="demo")

    @staticmethod
    def get_notification_by_username(username: str) -> ResultProxy:
        """
        Retrieve all the notifications for a user from the past two weeks
        :param username: Unique identifier for a user
        :return: A list of notifications
        """
        return db.session.execute(
            """
            SELECT * FROM notifications 
            WHERE username=:username 
            AND time >= CURDATE() - INTERVAL DAYOFWEEK(CURDATE()) + 13 DAY 
            AND deleted IS FALSE
            ORDER BY time DESC
            """,
            {"username": username},
            bind=NotificationDemoDao.engine,
        )
