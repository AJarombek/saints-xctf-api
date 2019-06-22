"""
Flair ORM model for the 'flair' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from app import db
from sqlalchemy import Column


class Flair(db.Model):
    __tablename__ = 'flair'

    flair_id = Column(db.INT, autoincrement=True, primary_key=True)
    username = Column(db.VARCHAR(20))
    flair = Column(db.VARCHAR(50))

    def __repr__(self):
        return '<Flair %r,%r>' % (self.username, self.flair)
