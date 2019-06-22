"""
Message ORM model for the 'messages' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Message(db.Model):
    __tablename__ = 'messages'

    message_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    group_name = Column(db.VARCHAR(20), nullable=False)
    time = Column(db.DATETIME, nullable=False)
    content = Column(db.VARCHAR(1000))

    def __repr__(self):
        return '<Message %r>' % self.message_id
