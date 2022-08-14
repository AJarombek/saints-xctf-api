"""
WeekStart ORM model for the 'admins' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from app import db
from model.Admin import Admin
from sqlalchemy import Column


class AdminDemo(Admin):
    __bind_key__ = 'demo'

    user = Column(db.TEXT, primary_key=True, nullable=False)
