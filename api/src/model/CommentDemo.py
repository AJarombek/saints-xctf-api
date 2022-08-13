"""
WeekStart ORM model for the 'comments' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Comment import Comment


class CommentDemo(Comment):
    __bind_key__ = 'demo'
