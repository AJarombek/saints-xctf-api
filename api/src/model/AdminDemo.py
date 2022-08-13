"""
WeekStart ORM model for the 'admins' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.Admin import Admin


class AdminDemo(Admin):
    __bind_key__ = 'demo'
