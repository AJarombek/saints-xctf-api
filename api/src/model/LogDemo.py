"""
WeekStart ORM model for the 'logs' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Log import Log


class LogDemo(Log):
    __bind_key__ = 'demo'
