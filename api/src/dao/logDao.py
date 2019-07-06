"""
Log data access from the SaintsXCTF MySQL database.  Contains exercise logs for users.
Author: Andrew Jarombek
Date: 7/3/2019
"""

import utils.dates as dates
from database import db
from model.Log import Log


class LogDao:

    @staticmethod
    def get_log_by_id(id: int) -> list:
        """
        Retrieve a specific exercise log based on its id number
        :param id:
        :return:
        """
        return Log.query.filter_by(log_id=id).all()

    @staticmethod
    def get_user_miles(username: str) -> dict:
        """
        Get the total exercise miles for a user
        :param username: Unique identifier for a user
        :return: The total number of miles exercised
        """
        return db.session.execute(
            '''
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            ''',
            {'username': username}
        )

    @staticmethod
    def get_user_miles_by_type(username: str, exercise_type: str):
        """
        Get the total miles of a certain exercise for a user
        :param username: Unique identifier for a user
        :param exercise_type: A certain type of exercise
        :return: The total number of miles exercised of a certain type
        """
        return db.session.execute(
            '''
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            AND type=:exercise_type
            ''',
            {'username': username, 'exercise_type': exercise_type}
        )

    @staticmethod
    def get_user_miles_interval(username: str, interval: str = None, week_start: str = 'monday') -> list:
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
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                ''',
                {'username': username}
            )
        else:
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND date >= :date
                ''',
                {'username': username, 'date': date}
            )

    @staticmethod
    def get_user_miles_interval_by_type(username: str, exercise_type: str,
                                        interval: str = None, week_start: str = 'monday') -> list:
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
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                AND type=:exercise_type
                ''',
                {'username': username, 'exercise_type': exercise_type}
            )
        else:
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND type=:exercise_type
                AND date >= :date
                ''',
                {'username': username, 'date': date, 'exercise_type': exercise_type}
            )

    @staticmethod
    def get_user_avg_feel(username: str):
        """
        Retrieve the average feel statistic for a user
        :param username: Unique identifier for a user
        :return: The average feel
        """
        return db.session.execute(
            '''
            SELECT AVG(feel) AS average 
            FROM logs 
            WHERE username=:username
            ''',
            {'username': username}
        )

    @staticmethod
    def get_user_avg_feel_interval(username: str, interval: str = None, week_start: str = 'monday'):
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
            return db.session.execute(
                '''
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                ''',
                {'username': username}
            )
        else:
            return db.session.execute(
                '''
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                AND date >= :date
                ''',
                {'username': username, 'date': date}
            )
