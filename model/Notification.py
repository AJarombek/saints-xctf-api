"""
Notification ORM model for the 'notification' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), nullable=False)
    time = Column(db.DATETIME, nullable=False)
    link = Column(db.VARCHAR(127))
    viewed = Column(db.CHAR(1), nullable=False)
    description = Column(db.VARCHAR(127))

    def __repr__(self):
        return '<Notification %r,%r>' % (self.username, self.description)
