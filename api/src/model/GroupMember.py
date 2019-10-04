"""
GroupMember ORM model for the 'groupmembers' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class GroupMember(db.Model):
    __tablename__ = 'groupmembers'

    id = Column(db.INTEGER, primary_key=True)
    group_name = Column(db.VARCHAR(20), db.ForeignKey('groups.group_name'), index=True)
    username = Column(db.VARCHAR(20), index=True)
    status = Column(db.VARCHAR(10), db.ForeignKey('status.status'))
    user = Column(db.VARCHAR(10), db.ForeignKey('admins.user'))

    def __repr__(self):
        return '<GroupMember %r,%r>' % (self.group_name, self.username)
