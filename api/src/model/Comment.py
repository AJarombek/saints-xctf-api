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

    __tablename__ = 'comments'

    comment_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    log_id = Column(db.INT, db.ForeignKey('logs.log_id'), nullable=False)
    time = Column(db.DATETIME, nullable=False)
    content = Column(db.VARCHAR(1000))

    def __repr__(self):
        return '<Comment %r>' % self.comment_id
