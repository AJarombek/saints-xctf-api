"""
Log data access from the SaintsXCTF MySQL database.  Contains exercise logs for users.
Author: Andrew Jarombek
Date: 9/14/2022
"""

from typing import Literal

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.schema import Column

from app import app
import utils.dates as dates
from database import db

WeekStart = Literal['monday', 'sunday']


class LogDemoDao:
    engine = db.get_engine(app=app, bind='demo')

    @staticmethod
    def get_user_miles(username: str) -> Column:
        """
        Get the total exercise miles for a user
        :param username: Unique identifier for a user
        :return: The total number of miles exercised
        """
        result: ResultProxy = db.session.execute(
            '''
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            AND deleted IS FALSE
            ''',
            {'username': username}
        )
        return result.first()

    @staticmethod
    def get_user_miles_interval(username: str, interval: str = None, week_start: WeekStart = 'monday') -> Column:
        """
        Get the total number of miles exercised by a user in a certain time interval.  The options include
        the past year, month, or week.
        :param username: Unique identifier for a user
        :param interval: Time interval for logs to count towards the mileage total
        :param week_start: An option for which day is used as the start of the week.
        Both 'monday' and 'sunday' are valid options.
        :return: The total number of miles exercised
        """
        date = dates.get_start_date_interval(interval=interval, week_start=week_start)

        if date is None:
            result: ResultProxy = db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                AND deleted IS FALSE
                ''',
                {'username': username},
                bind=LogDemoDao.engine
            )
        else:
            result: ResultProxy = db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND date >= :date
                AND deleted IS FALSE
                ''',
                {'username': username, 'date': date},
                bind=LogDemoDao.engine
            )

        return result.first()

    @staticmethod
    def get_user_miles_interval_by_type(
        username: str,
        exercise_type: str,
        interval: str = None,
        week_start: WeekStart = 'monday'
    ) -> Column:
        """
        Get the total number of miles exercised by a user in a certain time interval and specific exercise type.
        The interval options include the past year, month, and week.
        The exercise type options include run, bike, swim, and other.
        :param username: Unique identifier for a user
        :param interval: Time interval for logs to count towards the mileage total
        :param exercise_type: Type of exercise to filter the logs by
        :param week_start: An option for which day is used as the start of the week.
        Both 'monday' and 'sunday' are valid options.
        :return: The total number of miles for the given exercise type
        """
        date = dates.get_start_date_interval(interval=interval, week_start=week_start)

        if date is None:
            result: ResultProxy = db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                AND type=:exercise_type
                AND deleted IS FALSE
                ''',
                {'username': username, 'exercise_type': exercise_type},
                bind=LogDemoDao.engine
            )
        else:
            result: ResultProxy = db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND type=:exercise_type
                AND date >= :date
                AND deleted IS FALSE
                ''',
                {'username': username, 'date': date, 'exercise_type': exercise_type},
                bind=LogDemoDao.engine
            )

        return result.first()

    @staticmethod
    def get_user_avg_feel(username: str) -> Column:
        """
        Retrieve the average feel statistic for a user
        :param username: Unique identifier for a user
        :return: The average feel
        """
        result: ResultProxy = db.session.execute(
            '''
            SELECT AVG(feel) AS average 
            FROM logs 
            WHERE username=:username
            AND deleted IS FALSE
            ''',
            {'username': username},
            bind=LogDemoDao.engine
        )
        return result.first()

    @staticmethod
    def get_user_avg_feel_interval(username: str, interval: str = None, week_start: WeekStart = 'monday') -> Column:
        """
        Retrieve the average feel statistic for a user during a certain interval in time
        :param username: Unique identifier for a user
        :param interval: Time interval for logs to count towards the average feel
        :param week_start: An option for which day is used as the start of the week.
        Both 'monday' and 'sunday' are valid options.
        :return: The average feel during the interval
        """
        date = dates.get_start_date_interval(interval=interval, week_start=week_start)

        if date is None:
            result: ResultProxy = db.session.execute(
                '''
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                AND deleted IS FALSE
                ''',
                {'username': username},
                bind=LogDemoDao.engine
            )
        else:
            result: ResultProxy = db.session.execute(
                '''
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                AND date >= :date
                AND deleted IS FALSE
                ''',
                {'username': username, 'date': date},
                bind=LogDemoDao.engine
            )

        return result.first()
