"""
Message ORM model for the 'messages' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Message(db.Model):

    def __init__(self, message: dict):
        """
        Initialize a Message by passing in a dictionary.
        :param message: A dictionary with fields matching the Message fields
        """
        self.message_id = message.get('message_id')
        self.username = message.get('username')
        self.first = message.get('first')
        self.last = message.get('last')
        self.group_name = message.get('group_name')
        self.time = message.get('time')
        self.content = message.get('content')
        self.deleted = message.get('deleted')
        self.created_date = message.get('created_date')
        self.created_user = message.get('created_user')
        self.created_app = message.get('created_app')
        self.modified_date = message.get('modified_date')
        self.modified_user = message.get('modified_user')
        self.modified_app = message.get('modified_app')
        self.deleted_date = message.get('deleted_date')
        self.deleted_user = message.get('deleted_user')
        self.deleted_app = message.get('deleted_app')

    __tablename__ = 'messages'

    # Data Columns
    message_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), nullable=False)
    time = Column(db.DATETIME, nullable=False)
    content = Column(db.VARCHAR(1000))
    deleted = Column(db.CHAR(1))

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
        String representation of a group/team message.  This representation is meant to be human readable.
        :return: The message in string form.
        """
        return f'Message: [message_id: {self.message_id}, username: {self.username}, first: {self.first}, ' \
            f'last: {self.last}, group_name: {self.group_name}, time: {self.time}, content: {self.content}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a group/team message.  This representation is meant to be machine readable.
        :return: The message in string form.
        """
        return '<Message %r>' % self.message_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group/team message.
        :return: True if the objects are equal, False otherwise.
        """
        return Message.compare(self, other)

    @classmethod
    def compare(cls, message_1, message_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be messages.
        :param message_1: The first message object.
        :param message_2: The second message object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            message_1.message_id == message_2.message_id,
            message_1.username == message_2.username,
            message_1.first == message_2.first,
            message_1.last == message_2.last,
            message_1.group_name == message_2.group_name,
            str(message_1.time) == str(message_2.time),
            message_1.content == message_2.content,
            message_1.deleted == message_2.deleted
        ])
