"""
WeekStart ORM model for the 'types' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from sqlalchemy import Column

from app import db
from model.Type import Type


class TypeDemo(Type):
    __bind_key__ = "demo"

    type = Column(db.TEXT, primary_key=True, nullable=False)
