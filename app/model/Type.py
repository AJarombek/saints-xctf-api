"""
Type ORM model for the 'types' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Type(db.Model):
    __tablename__ = 'types'

    type = Column(db.VARCHAR(15), primary_key=True)

    log = db.relationship('Log', backref='log')

    def __repr__(self):
        return '<Type %r>' % self.type
