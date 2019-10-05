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
    def get_activation_code(code: str) -> list:
        """
        Retrieve a single activation code by its unique characters.
        :param code: An activation code.
        :return: The result of the query.
        """
        return Code.query.filter_by(activation_code=code).first()

    @staticmethod
    def activation_code_exists(activation_code: str) -> dict:
        """
        Retrieve the count of activation codes that match an identifier.
        :param activation_code: Random characters that make up an activation code.
        :return: The result of the query.
        """
        return db.session.execute(
            '''
            SELECT COUNT(*) AS 'exists' 
            FROM codes 
            WHERE activation_code=:activation_code
            ''',
            {'activation_code': activation_code}
        )

    @staticmethod
    def add_activation_code(new_code: Code) -> bool:
        """
        Add an activation code to the database.
        :param new_code: Object representing an activation code for a user.
        :return: True if the code is inserted into the database, False otherwise.
        """
        db.session.add(new_code)
        return BasicDao.safe_commit()

    @staticmethod
    def delete_code(activation_code: str) -> bool:
        """
        Delete an activation code from the database based on its code.
        :param activation_code: An activation code.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM codes WHERE activation_code=:activation_code',
            {'activation_code': activation_code}
        )
        return BasicDao.safe_commit()
