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
        :param flair: A dictionary with fields matching the Flair fields
        """
        self.username = flair.get('username')
        self.flair = flair.get('flair')

    __tablename__ = 'flair'

    flair_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'))
    flair = Column(db.VARCHAR(50))

    def __repr__(self):
        return '<Flair %r,%r>' % (self.username, self.flair)
