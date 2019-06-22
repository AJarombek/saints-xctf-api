"""
Event ORM model for the 'events' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Event(db.Model):
    __tablename__ = 'events'

    event_id = Column(db.INT, autoincrement=True, primary_key=True)
    name = Column(db.VARCHAR(40), nullable=False)
    group_name = Column(db.VARCHAR(20), nullable=False)
    start_date = Column(db.DATE, nullable=False)
    end_date = Column(db.DATE)
    start_time = Column(db.TIME)
    description = Column(db.VARCHAR(1000))

    def __repr__(self):
        return '<Event %r>' % self.name
