"""
Code data access from the SaintsXCTF MySQL database.  Contains SQL queries related to user activation codes.
Author: Andrew Jarombek
Date: 6/23/2019
"""

from app import db, app
from dao.basicDao import BasicDao
from model.Code import Code


class CodeDao:

    @staticmethod
    def get_code_count(activation_code: str) -> int:
        """
        Get the number of activation codes matching a string.
        :param activation_code: String representing an activation code for a user.
        :return: The number of codes.
        """
        return Code.query.filter_by(activation_code=activation_code).count()

    @staticmethod
    def remove_code(code: Code) -> bool:
        """
        Delete an activation code from the database.
        :param code: Object model for a row in the code table.
        :return: True if the activation code is deleted, False otherwise.
        """
        db.session.remove(code)
        return BasicDao.safe_commit()