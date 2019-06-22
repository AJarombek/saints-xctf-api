"""
Group ORM model for the 'groups' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGBLOB


class Group(db.Model):
    __tablename__ = 'groups'

    group_name = Column(db.VARCHAR(20), primary_key=True)
    group_title = Column(db.VARCHAR(50))
    grouppic = Column(LONGBLOB)
    grouppic_name = Column(db.VARCHAR(50))
    week_start = Column(db.VARCHAR(15))
    description = Column(db.VARCHAR(255))

    def __repr__(self):
        return '<Group %r>' % self.group_name
