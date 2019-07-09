"""
Log data access from the SaintsXCTF MySQL database.  Contains exercise logs for users.
Author: Andrew Jarombek
Date: 7/3/2019
"""

import utils.dates as dates
from dao.basicDao import BasicDao
from database import db
from model.Log import Log


class LogDao:

    @staticmethod
    def get_logs() -> list:
        """
        Retrieve all the exercise logs in the database
        :return: The result of the query.
        """
        return Log.query.order_by(Log.date).all()

    @staticmethod
    def get_log_by_id(log_id: int) -> list:
        """
        Retrieve a specific exercise log based on its id number
        :param log_id: Unique identifier for an exercise log.
        :return: The result of the query.
        """
        return Log.query.filter_by(log_id=log_id).all()

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
    def get_user_miles_by_type(username: str, exercise_type: str) -> dict:
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
    def get_user_avg_feel_interval(username: str, interval: str = None, week_start: str = 'monday') -> list:
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

    @staticmethod
    def get_group_miles(group_name: str):
        """
        Get the total exercise miles for all the users in a group.
        :param group_name: Unique name for a group.
        :return: The total number of miles exercised.
        """
        return db.session.execute(
            '''
            SELECT SUM(miles) AS total 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:team 
            AND status='accepted'
            ''',
            {'group_name': group_name}
        )

    @staticmethod
    def get_group_miles_interval(group_name: str, interval: str = None, week_start: str = 'monday'):
        """
        Get the total number of miles exercised by all the group members in a certain time interval.  The time interval
        options include the past year, month, or week.
        :param group_name: Name which uniquely identifies for a group
        :param interval: Time interval for logs to count towards the mileage total
        :param week_start: An option for which day is used as the start of the week.
        Both 'monday' and 'sunday' are valid options.
        :return: The total number of miles exercised
        """
        date = dates.get_start_date_interval(interval=interval, week_start=week_start)

        if date is None:
            return db.session.execute(
                '''
                select sum(miles) as total 
                from logs 
                inner join groupmembers on logs.username = groupmembers.username 
                where group_name=:group_name
                and status='accepted'
                ''',
                {'group_name': group_name}
            )
        else:
            return db.session.execute(
                '''
                select sum(miles) as total 
                from logs 
                inner join groupmembers on logs.username = groupmembers.username 
                where group_name=:group_name 
                and date >= :date 
                and status='accepted'
                ''',
                {'group_name': group_name, 'date': date}
            )

    @staticmethod
    def add_log(new_log: Log) -> bool:
        """
        Add an exercise log to the database.
        :param new_log: Object representing an exercise log for a user.
        :return: True if the log is inserted into the database, False otherwise.
        """
        db.session.add(new_log)
        return BasicDao.safe_commit()

    @staticmethod
    def update_log(log: Log) -> bool:
        """
        Update a log in the database.
        :param log: Object representing an updated log.
        :return: True if the log is updated in the database, False otherwise.
        """
        db.session.add(log)
        return BasicDao.safe_commit()

    @staticmethod
    def delete_log(log_id: int) -> bool:
        """
        Delete a log from the database based on its id.
        :param log_id: ID which uniquely identifies the log.
        :return: True if the deletion was successful without error, False otherwise.
        """
        db.session.execute(
            'DELETE FROM logs WHERE log_id=:log_id',
            {'log_id': log_id}
        )
        return BasicDao.safe_commit()
