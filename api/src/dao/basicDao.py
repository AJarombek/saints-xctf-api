"""
Basic Data Access Object with function reused by the other DAOs.
Author: Andrew Jarombek
Date: 6/23/2019
"""

from app import db, app
from sqlalchemy.exc import SQLAlchemyError


class BasicDao:

    @staticmethod
    def safe_commit() -> bool:
        """
        Safely attempt to commit changes to MySQL.  Rollback in case of a failure.
        :return: True if the commit was successful, False if a rollback occurred.
        """
        try:
            db.session.commit()
            app.logger.info('SQL Safely Committed')
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            app.logger.error('SQL Commit Failed!  Rolling back...')
            app.logger.error(error.args)
            return False
