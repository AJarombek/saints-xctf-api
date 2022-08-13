"""
WeekStart ORM model for the 'weekstart' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class WeekStart(db.Model):
    __tablename__ = 'weekstart'
    __bind_key__ = 'app'

    week_start = Column(db.VARCHAR(15), primary_key=True)

    user = db.relationship('User', backref='user')
    group = db.relationship('Group', backref='group')

    def __repr__(self):
        """
        String representation of the start of week options.  This representation is meant to be machine readable.
        :return: The week start object in string form.
        """
        return '<WeekStart %r>' % self.week_start


class WeekStartDemo(WeekStart):
    __bind_key__ = 'demo'
