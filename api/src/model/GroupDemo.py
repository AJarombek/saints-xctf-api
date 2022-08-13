"""
WeekStart ORM model for the 'groups' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Group import Group


class GroupDemo(Group):
    __bind_key__ = 'demo'
