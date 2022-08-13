"""
WeekStart ORM model for the 'flair' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Flair import Flair


class FlairDemo(Flair):
    __bind_key__ = 'demo'
