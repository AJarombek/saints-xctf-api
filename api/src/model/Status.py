"""
Status ORM model for the 'status' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Status(db.Model):
    __tablename__ = "status"

    status = Column(db.VARCHAR(10), primary_key=True)

    group_members = db.relationship("GroupMember", backref="group_member")

    def __repr__(self):
        return "<Status %r>" % self.status
