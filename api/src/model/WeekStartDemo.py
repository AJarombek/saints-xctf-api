"""
WeekStart ORM model for the 'weekstart' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.WeekStart import WeekStart


class WeekStartDemo(WeekStart):
    __bind_key__ = 'demo'
