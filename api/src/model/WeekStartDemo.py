"""
WeekStart ORM model for the 'weekstart' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.WeekStart import WeekStart


class WeekStartDemo(WeekStart):
    __bind_key__ = 'demo'

    week_start = Column(db.TEXT, primary_key=True, nullable=False)
