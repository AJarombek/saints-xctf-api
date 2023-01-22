"""
Basic Data Access Object with function reused by the other DAOs.
Author: Andrew Jarombek
Date: 6/23/2019
"""

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from database import db


class BasicDao:
    @staticmethod
    def safe_commit() -> bool:
        """
        Safely attempt to commit changes to MySQL.  Rollback in case of a failure.
        :return: True if the commit was successful, False if a rollback occurred.
        """
        try:
            # pylint: disable=no-member
            db.session.commit()
            current_app.logger.info("SQL Safely Committed")
            return True
        except SQLAlchemyError as error:
            # pylint: disable=no-member
            db.session.rollback()
            current_app.logger.error("SQL Commit Failed!  Rolling back...")
            current_app.logger.error(error.args)
            return False
