"""
Admin ORM model for the 'admins' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Admin(db.Model):
    __tablename__ = 'admins'

    user = Column(db.VARCHAR(10), primary_key=True)

    group_members = db.relationship('GroupMember', backref='group_member')

    def __repr__(self):
        return '<Admin %r>' % self.user
