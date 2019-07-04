"""
ForgotPassword data access from the SaintsXCTF MySQL database.  Contains SQL queries related to codes users
are given when they forget their password.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from database import db
from model.ForgotPassword import ForgotPassword


class ForgotPasswordDao:

    @staticmethod
    def get_forgot_password_codes(username: str) -> list:
        """
        Retrieve all the forgot password codes that aren't expired yet for a user
        :param username: The unique identifier for a user
        :return: A list of forgot password codes
        """
        return db.session.execute(
            '''
            SELECT forgot_code 
            FROM forgotpassword 
            WHERE username=:username 
            AND expires >= NOW()
            ''',
            {'username': username}
        )
