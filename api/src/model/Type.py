"""
Type ORM model for the 'types' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from sqlalchemy import Column

from app import db


class Type(db.Model):
    def __init__(self, exercise_type: dict):
        """
        Initialize a Type by passing in a dictionary.
        :param exercise_type: A dictionary with fields matching the Type fields
        """
        self.type = exercise_type.get("type")

    __tablename__ = "types"

    type = Column(db.VARCHAR(15), primary_key=True)

    def __str__(self):
        """
        String representation of an exercise log type.  This representation is meant to be human-readable.
        :return: The type in string form.
        """
        return f"Type: [type: {self.type}]"

    def __repr__(self):
        """
        String representation of an exercise log type.  This representation is meant to be machine-readable.
        :return: The type in string form.
        """
        return f"<Type '{self.type}'>"

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this type.
        :return: True if the objects are equal, False otherwise.
        """
        return self.type == other.type
