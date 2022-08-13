"""
WeekStart ORM model for the 'notifications' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Notification import Notification


class NotificationDemo(Notification):
    __bind_key__ = 'demo'
