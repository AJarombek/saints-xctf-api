"""
ForgotPassword ORM model for the 'forgotpassword' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class ForgotPassword(db.Model):

    def __init__(self, forgot_password: dict):
        """
        Initialize a ForgotPassword object by passing in a dictionary.
        :param forgot_password: A dictionary with fields matching the ForgotPassword fields
        """
        self.forgot_code = forgot_password.get('forgot_code')
        self.username = forgot_password.get('username')
        self.expires = forgot_password.get('expires')
        self.deleted = forgot_password.get('deleted')
        self.created_date = forgot_password.get('created_date')
        self.created_user = forgot_password.get('created_user')
        self.created_app = forgot_password.get('created_app')
        self.modified_date = forgot_password.get('modified_date')
        self.modified_user = forgot_password.get('modified_user')
        self.modified_app = forgot_password.get('modified_app')
        self.deleted_date = forgot_password.get('deleted_date')
        self.deleted_user = forgot_password.get('deleted_user')
        self.deleted_app = forgot_password.get('deleted_app')

    __tablename__ = 'forgotpassword'

    # Data Columns
    forgot_code = Column(db.VARCHAR(8), primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False, index=True)
    expires = Column(db.DATETIME, nullable=False)
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
        String representation of a forgot password code.  This representation is meant to be human readable.
        :return: The forgot password code in string form.
        """
        return f'ForgotPassword: [forgot_code: {self.forgot_code}, username: {self.username}, ' \
            f'expires: {self.expires}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a forgot password code.  This representation is meant to be machine readable.
        :return: The forgot password code in string form.
        """
        return '<ForgotPassword %r,%r>' % (self.forgot_code, self.username)
