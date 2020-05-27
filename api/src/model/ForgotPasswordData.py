"""
Forgot Password model that only includes data columns.
Author: Andrew Jarombek
Date: 11/5/2019
"""

from typing import Optional

from .ForgotPassword import ForgotPassword


class ForgotPasswordData:

    def __init__(self, forgot_password: Optional[ForgotPassword]):
        """
        Create a forgot password object without any auditing fields.
        :param forgot_password: The original Forgot Password object with auditing fields.
        """
        if forgot_password is not None:
            self.forgot_code = forgot_password.forgot_code
            self.username = forgot_password.username
            self.expires = forgot_password.expires
            self.deleted = forgot_password.deleted

    def __str__(self):
        """
        String representation of a forgot password code.  This representation is meant to be human readable.
        :return: The forgot password code in string form.
        """
        return f'ForgotPasswordData: [forgot_code: {self.forgot_code}, username: {self.username}, ' \
            f'expires: {self.expires}, deleted: {self.deleted}]'

    def __repr__(self):
        """
        String representation of a forgot password code.  This representation is meant to be machine readable.
        :return: The forgot password code in string form.
        """
        return '<ForgotPasswordData %r,%r>' % (self.forgot_code, self.username)

    def __eq__(self, other):
        """
        Determine value equality between this object and another object.
        :param other: Another object to compare to this forgot password code.
        :return: True if the objects are equal, False otherwise.
        """
        return ForgotPassword.compare(self, other)
