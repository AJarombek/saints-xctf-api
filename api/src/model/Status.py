"""
Status ORM model for the 'status' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from sqlalchemy import Column

from app import db


class Status(db.Model):
    __tablename__ = "status"

    status = Column(db.VARCHAR(10), primary_key=True)

    group_members = db.relationship("GroupMember", backref="group_member")

    def __repr__(self):
        """
        String representation of a group member status.  This representation is meant to be machine-readable.
        :return: The group member status in string form.
        """
        return f"<Status '{self.status}'>"
