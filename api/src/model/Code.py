"""
Code ORM model for the 'codes' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class Code(db.Model):

    def __init__(self, code: dict):
        """
        Initialize a Code by passing in a dictionary.
        :param code: A dictionary with fields matching the Code fields
        """
        self.activation_code = code.get('activation_code')
        self.deleted = code.get('deleted')
        self.created_date = code.get('created_date')
        self.created_user = code.get('created_user')
        self.created_app = code.get('created_app')
        self.modified_date = code.get('modified_date')
        self.modified_user = code.get('modified_user')
        self.modified_app = code.get('modified_app')
        self.deleted_date = code.get('deleted_date')
        self.deleted_user = code.get('deleted_user')
        self.deleted_app = code.get('deleted_app')

    __tablename__ = 'codes'

    # Data Columns
    activation_code = Column(db.VARCHAR(8), primary_key=True)
    deleted = Column(db.CHAR(1))

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
        String representation of an activation code.  This representation is meant to be human readable.
        :return: The activation code string.
        """
        return f'Code: [activation_code: {self.activation_code}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of an activation code.  This representation is meant to be machine readable.
        :return: The activation code string.
        """
        return '<Code %r>' % self.activation_code
