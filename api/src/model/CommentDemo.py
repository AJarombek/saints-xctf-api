"""
WeekStart ORM model for the 'comments' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from app import db
from model.Comment import Comment
from sqlalchemy import Column


class CommentDemo(Comment):
    __bind_key__ = 'demo'

    # Data Columns
    comment_id = Column(db.INTEGER, autoincrement=True, primary_key=True)
    username = Column(db.TEXT, db.ForeignKey('users.username'), nullable=False)
    first = Column(db.TEXT, nullable=False)
    last = Column(db.TEXT, nullable=False)
    log_id = Column(db.INTEGER, db.ForeignKey('logs.log_id'), nullable=False)
    time = Column(db.NUMERIC, nullable=False)
    content = Column(db.TEXT)
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
