"""
ForgotPassword data access from the SaintsXCTF demo database.  Contains SQL queries related to codes users
are given when they forget their password.
Author: Andrew Jarombek
Date: 9/13/2022
"""

from sqlalchemy.engine.cursor import ResultProxy

from app import app
from database import db


class ForgotPasswordDemoDao:
    engine = db.get_engine(app=app, bind='demo')

    @staticmethod
    def get_forgot_password_codes(username: str) -> ResultProxy:
        """
        Retrieve all the forgot password codes that aren't expired yet for a user
        :param username: The unique identifier for a user
        :return: A list of forgot password codes
        """
        return db.session.execute(
            '''
            SELECT forgot_code, username, expires, deleted 
            FROM forgotpassword 
            WHERE username=:username 
            AND expires >= NOW()
            AND deleted IS FALSE
            ''',
            {'username': username},
            bind=ForgotPasswordDemoDao.engine
        )
