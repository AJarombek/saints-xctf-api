"""
Comment ORM model for the 'comments' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Comment(db.Model):

    def __init__(self, comment: dict):
        """
        Initialize a Comment by passing in a dictionary.
        :param comment: A dictionary with fields matching the Comment fields
        """
        self.comment_id = comment.get('comment_id')
        self.username = comment.get('username')
        self.first = comment.get('first')
        self.last = comment.get('last')
        self.log_id = comment.get('log_id')
        self.time = comment.get('time')
        self.content = comment.get('content')
        self.deleted = comment.get('deleted')
        self.created_date = comment.get('created_date')
        self.created_user = comment.get('created_user')
        self.created_app = comment.get('created_app')
        self.modified_date = comment.get('modified_date')
        self.modified_user = comment.get('modified_user')
        self.modified_app = comment.get('modified_app')
        self.deleted_date = comment.get('deleted_date')
        self.deleted_user = comment.get('deleted_user')
        self.deleted_app = comment.get('deleted_app')

    __tablename__ = 'comments'

    # Data Columns
    comment_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    log_id = Column(db.INT, db.ForeignKey('logs.log_id'), nullable=False)
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

    def __repr__(self):
        """
        String representation of the comment.
        :return: The comment string.
        """
        return '<Comment %r>' % self.comment_id

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Comment.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            self.comment_id == other.comment_id,
            self.username == other.username,
            self.first == other.first,
            self.last == other.last,
            self.log_id == other.log_id,
            self.time == other.time,
            self.content == other.content,
            self.deleted == other.deleted
        ])
