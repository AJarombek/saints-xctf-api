"""
WeekStart ORM model for the 'weekstart' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from sqlalchemy import Column

from app import db


class WeekStart(db.Model):
    __tablename__ = "weekstart"

    week_start = Column(db.VARCHAR(15), primary_key=True)

    user = db.relationship("User", backref="user")
    group = db.relationship("Group", backref="group")

    def __repr__(self):
        """
        String representation of the start of week options.  This representation is meant to be machine readable.
        :return: The week start object in string form.
        """
        return f"<WeekStart {self.week_start}>"
