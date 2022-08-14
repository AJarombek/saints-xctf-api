"""
WeekStart ORM model for the 'status' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Status import Status


class StatusDemo(Status):
    __bind_key__ = 'demo'

    status = Column(db.TEXT, primary_key=True, nullable=False)
