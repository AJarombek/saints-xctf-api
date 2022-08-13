"""
WeekStart ORM model for the 'status' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Status import Status


class StatusDemo(Status):
    __bind_key__ = 'demo'
