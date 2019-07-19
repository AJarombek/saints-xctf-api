"""
Message ORM model for the 'messages' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Message(db.Model):

    def __init__(self, log: dict):
        """
        Initialize a Message by passing in a dictionary.
        :param log: A dictionary with fields matching the Message fields
        """
        self.message_id = log.get('message_id')
        self.username = log.get('username')
        self.first = log.get('first')
        self.last = log.get('last')
        self.group_name = log.get('group_name')
        self.time = log.get('time')
        self.content = log.get('content')

    __tablename__ = 'messages'

    message_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), nullable=False)
    time = Column(db.DATETIME, nullable=False)
    content = Column(db.VARCHAR(1000))

    def __repr__(self):
        return '<Message %r>' % self.message_id
