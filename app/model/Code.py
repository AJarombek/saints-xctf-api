"""
Code ORM model for the 'codes' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Code(db.Model):
    __tablename__ = 'codes'

    activation_code = Column(db.VARCHAR(8), primary_key=True)

    def __repr__(self):
        return '<Code %r>' % self.activation_code
