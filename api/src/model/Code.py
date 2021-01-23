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
        self.email = code.get('email')
        self.group_id = code.get('group_id')
        self.expiration_date = code.get('expiration_date')
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
    email = Column(db.VARCHAR(50), index=True)
    group_id = Column(db.INTEGER, db.ForeignKey('groups.id'))
    expiration_date = Column(db.DATETIME)
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
        return f'Code: [activation_code: {self.activation_code}, email: {self.email}, group_id: {self.group_id}, ' \
               f'expiration_date: {self.expiration_date}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of an activation code.  This representation is meant to be machine readable.
        :return: The activation code string.
        """
        return '<Code %r>' % self.activation_code

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this Code.
        :return: True if the objects are equal, False otherwise.
        """
        return Code.compare(self, other)

    @classmethod
    def compare(cls, code1, code2) -> bool:
        """
        Helper function used to determine value equality between two objects that are assumed to be activation
        codes for users.
        :param code1: The first activation code object.
        :param code2: The second activation code object.
        :return: True if the objects are equal, False otherwise.
        """
        return all([
            code1.activation_code == code2.activation_code,
            code1.email == code2.email,
            code1.group_id == code2.group_id,
            code1.expiration_date == code2.expiration_date,
            code1.deleted == code2.deleted
        ])
