"""
WeekStart ORM model for the 'forgotpassword' table in the demo SQLite database.
Author: Andrew Jarombek
Date: 8/13/2022
"""

from model.ForgotPassword import ForgotPassword


class ForgotPasswordDemo(ForgotPassword):
    __bind_key__ = 'demo'
