"""
WeekStart ORM model for the 'notifications' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Notification import Notification


class NotificationDemo(Notification):
    __bind_key__ = "demo"

    # Data Columns
    notification_id = Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = Column(db.TEXT, db.ForeignKey("users.username"), nullable=False)
    time = Column(db.NUMERIC, nullable=False)
    link = Column(db.TEXT)
    viewed = Column(db.TEXT, nullable=False)
    description = Column(db.TEXT)
    deleted = Column(db.INTEGER)

    # Audit Columns
    created_date = Column(db.NUMERIC)
    created_user = Column(db.TEXT)
    created_app = Column(db.TEXT)
    modified_date = Column(db.NUMERIC)
    modified_user = Column(db.TEXT)
    modified_app = Column(db.TEXT)
    deleted_date = Column(db.NUMERIC)
    deleted_user = Column(db.TEXT)
    deleted_app = Column(db.TEXT)
