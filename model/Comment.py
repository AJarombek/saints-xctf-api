"""
Comment ORM model for the 'comments' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), nullable=False)
    first = Column(db.VARCHAR(30), nullable=False)
    last = Column(db.VARCHAR(30), nullable=False)
    log_id = Column(db.INT, nullable=False)
    time = Column(db.DATETIME, nullable=False)
    content = Column(db.VARCHAR(1000))

    def __repr__(self):
        return '<Comment %r>' % self.comment_id
