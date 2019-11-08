"""
Forgot Password model that only includes data columns.
Author: Andrew Jarombek
Date: 11/5/2019
"""

from .ForgotPassword import ForgotPassword


class ForgotPasswordData:
    def __init__(self, forgot_password: ForgotPassword):
        """
        Create a forgot password object without any auditing fields.
        :param forgot_password: The original Forgot Password object with auditing fields.
        """
        self.forgot_code = forgot_password.forgot_code
        self.username = forgot_password.username
        self.expires = forgot_password.expires
        self.deleted = forgot_password.deleted
