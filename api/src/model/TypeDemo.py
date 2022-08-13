"""
WeekStart ORM model for the 'types' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Type import Type


class TypeDemo(Type):
    __bind_key__ = 'demo'
