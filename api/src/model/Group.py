"""
Group ORM model for the 'groups' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGBLOB


class Group(db.Model):
    def __init__(self, group: dict):
        """
        Initialize a Group object by passing in a dictionary.
        :param group: A dictionary with fields matching the Group fields
        """
        self.id = group.get("id")
        self.group_name = group.get("group_name")
        self.group_title = group.get("group_title")
        self.grouppic = group.get("grouppic")
        self.grouppic_name = group.get("grouppic_name")
        self.week_start = group.get("week_start")
        self.description = group.get("description")
        self.deleted = group.get("deleted")
        self.created_date = group.get("created_date")
        self.created_user = group.get("created_user")
        self.created_app = group.get("created_app")
        self.modified_date = group.get("modified_date")
        self.modified_user = group.get("modified_user")
        self.modified_app = group.get("modified_app")
        self.deleted_date = group.get("deleted_date")
        self.deleted_user = group.get("deleted_user")
        self.deleted_app = group.get("deleted_app")

    __tablename__ = "groups"
    __bind_key__ = "app"

    # Data Columns
    id = Column(db.INT, autoincrement=True, primary_key=True)
    group_name = Column(db.VARCHAR(20), index=True)
    group_title = Column(db.VARCHAR(50), index=True)
    grouppic = Column(LONGBLOB)
    grouppic_name = Column(db.VARCHAR(50))
    week_start = Column(db.VARCHAR(15), db.ForeignKey("weekstart.week_start"))
    description = Column(db.VARCHAR(255))
    deleted = Column(db.BOOLEAN)

    # Audit Columns
    created_date = Column(db.DATETIME)
    created_user = Column(db.VARCHAR(31))
    created_app = Column(db.VARCHAR(31))
    modified_date = Column(db.DATETIME)
    modified_user = Column(db.VARCHAR(31))
    modified_app = Column(db.VARCHAR(31))
    deleted_date = Column(db.DATETIME)
    deleted_user = Column(db.VARCHAR(31))
    deleted_app = Column(db.VARCHAR(31))

    def __str__(self):
        """
        String representation of a group within a team.  This representation is meant to be human readable.
        :return: The group in string form.
        """
        return (
            f"Group: [id: {self.id}, group_name: {self.group_name}, group_title: {self.group_title}, "
            f"grouppic: {self.grouppic}, grouppic_name: {self.grouppic_name}, week_start: {self.week_start}, "
            f"description: {self.description}, deleted: {self.deleted}]"
        )

    def __repr__(self):
        """
        String representation of a group within a team.  This representation is meant to be machine readable.
        :return: The group in string form.
        """
        return "<Group %r, %r>" % (self.id, self.group_name)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this group.
        :return: True if the objects are equal, False otherwise.
        """
        return Group.compare(self, other)

    @classmethod
    def compare(cls, group_1, group_2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be groups of athletes.
        :param group_1: The first group object.
        :param group_2: The second group object.
        :return: True if the objects are equal, False otherwise.
        """
        return all(
            [
                group_1.id == group_2.id,
                group_1.group_name == group_2.group_name,
                group_1.group_title == group_2.group_title,
                group_1.grouppic_name == group_2.grouppic_name,
                group_1.week_start == group_2.week_start,
                group_1.description == group_2.description,
            ]
        )
