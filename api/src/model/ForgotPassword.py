"""
ForgotPassword ORM model for the 'forgotpassword' table in the SaintsXCTF MySQL database.
Author: Andrew Jarombek
Date: 6/22/2019
"""

from app import db
from sqlalchemy import Column


class ForgotPassword(db.Model):

    def __init__(self, user: dict):
        """
        Initialize a ForgotPassword object by passing in a dictionary.
        :param user: A dictionary with fields matching the ForgotPassword fields
        """
        self.forgot_code = user.get('forgot_code')
        self.username = user.get('username')
        self.expires = user.get('expires')

    __tablename__ = 'forgotpassword'

    forgot_code = Column(db.VARCHAR(8), primary_key=True)
    username = Column(db.VARCHAR(20), db.ForeignKey('users.username'), nullable=False, index=True)
    expires = Column(db.DATETIME, nullable=False)

    def __repr__(self):
        return '<ForgotPassword %r,%r>' % (self.forgot_code, self.username)
