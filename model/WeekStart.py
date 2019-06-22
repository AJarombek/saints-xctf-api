"""
WeekStart ORM model for the 'weekstart' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class WeekStart(db.Model):
    __tablename__ = 'weekstart'

    week_start = Column(db.VARCHAR(15), primary_key=True)

    def __repr__(self):
        return '<WeekStart %r>' % self.week_start
