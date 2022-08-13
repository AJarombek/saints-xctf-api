"""
Flair ORM model for the 'flair' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from app import db
from sqlalchemy import Column


class Flair(db.Model):

    def __init__(self, flair: dict) -> None:
        """
        Initialize a Flair object by passing in a dictionary.
        :param flair: A dictionary with fields matching the Flair fields.
        """
        self.flair_id = flair.get('flair_id')
        self.username = flair.get('username')
        self.flair = flair.get('flair')
        self.deleted = flair.get('deleted')
        self.created_date = flair.get('created_date')
        self.created_user = flair.get('created_user')
        self.created_app = flair.get('created_app')
        self.modified_date = flair.get('modified_date')
        self.modified_user = flair.get('modified_user')
        self.modified_app = flair.get('modified_app')
        self.deleted_date = flair.get('deleted_date')
        self.deleted_user = flair.get('deleted_user')
        self.deleted_app = flair.get('deleted_app')

    __tablename__ = 'flair'
    __bind_key__ = 'app'

    # Data Columns
    flair_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'))
    flair = Column(db.VARCHAR(50))
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
        String representation of the user's flair.  This representation is meant to be human readable.
        :return: The flair in string form.
        """
        return f'Flair: [flair_id: {self.flair_id}, username: {self.username}, flair: {self.flair}, ' \
            f'deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of the user's flair.  This representation is meant to be machine readable.
        :return: The flair in string form.
        """
        return '<Flair %r,%r>' % (self.flair_id, self.username)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Flair.
        :return: True if the objects are equal, False otherwise.
        """
        return Flair.compare(self, other)

    @classmethod
    def compare(cls, flair1, flair2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be user's flair.
        :param flair1: The first flair object.
        :param flair2: The second flair object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            flair1.flair_id == flair2.flair_id,
            flair1.username == flair2.username,
            flair1.flair == flair2.flair,
            flair1.deleted == flair2.deleted
        ])
