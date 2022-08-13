"""
WeekStart ORM model for the 'users' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.User import User


class WeekStartDemo(User):
    __bind_key__ = 'demo'
