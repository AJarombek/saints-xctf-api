"""
ActivationCode data access from the SaintsXCTF MySQL database.  Contains codes used for activating user accounts.
Author: Andrew Jarombek
Date: 8/6/2019
"""

from database import db
from dao.basicDao import BasicDao
from model.Code import Code


class ActivationCodeDao:

    @staticmethod
    def get_activation_codes() -> list:
        pass
