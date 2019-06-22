"""
GroupMember ORM model for the 'groupmembers' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class GroupMember(db.Model):
    __tablename__ = 'groupmembers'

    group_name = Column(db.VARCHAR(20))
    username = Column(db.VARCHAR(20))
    status = Column(db.VARCHAR(10))
    user = Column(db.VARCHAR(10))

    def __repr__(self):
        return '<GroupMember %r,%r>' % (self.group_name, self.username)
