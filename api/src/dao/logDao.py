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
    def get_user_miles(username: str) -> dict:
        return db.session.execute(
            '''
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            ''',
            {'username': username}
        )

    @staticmethod
    def get_user_miles_interval(username: str, interval: str, week_start: str = 'monday') -> list:

        date = None
        if interval == 'year':
            date = dates.get_first_day_of_year()
        elif interval == 'month':
            date = dates.get_first_day_of_month()
        elif interval == 'week':
            date = dates.get_first_day_of_week(week_start=week_start)

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