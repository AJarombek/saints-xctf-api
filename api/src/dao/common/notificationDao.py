"""
Common Notification data access functions.  Contains notifications for events users should be aware of.
Author: Andrew Jarombek
Date: 11/5/2022
"""

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.engine import Engine

from database import db


class NotificationCommonDao:
    @staticmethod
    def get_notification_by_username(engine: Engine, username: str) -> ResultProxy:
        """
        Retrieve all the notifications for a user from the past two weeks
        :param engine: Engine (database connection details) to use for the database request
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
            bind=engine,
        )
