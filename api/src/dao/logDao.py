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
    def get_user_avg_feel(username: str) -> dict:
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
                SELECT SUM(miles) AS total 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name
                AND status='accepted'
                ''',
                {'group_name': group_name}
            )
        else:
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND date >= :date 
                AND status='accepted'
                ''',
                {'group_name': group_name, 'date': date}
            )

    @staticmethod
    def get_group_miles_interval_by_type(group_name: str, exercise_type: str,
                                         interval: str = None, week_start: str = 'monday'):
        """
        Get the total number of miles exercised by all the group members in a certain time interval and of a specific
        exercise type.  The interval options include the past year, month, and week.
        The exercise type options include run, bike, swim, and other.
        :param group_name: A name which uniquely identifies a group.
        :param interval: Time interval for logs to count towards the mileage total.
        :param exercise_type: Type of exercise to filter the logs by.
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
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND type=:exercise_type
                AND status='accepted'
                ''',
                {'group_name': group_name, 'exercise_type': exercise_type}
            )
        else:
            return db.session.execute(
                '''
                SELECT SUM(miles) AS total 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND type=:exercise_type
                AND date >= :date 
                AND status='accepted'
                ''',
                {'group_name': group_name, 'exercise_type': exercise_type, 'date': date}
            )

    @staticmethod
    def get_group_avg_feel(group_name: str) -> dict:
        """
        Retrieve the average feel statistic for a group.
        :param group_name: A name which uniquely identifies a group.
        :return: The average feel.
        """
        return db.session.execute(
            '''
            SELECT AVG(feel) AS average 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND status='accepted'
            ''',
            {'group_name': group_name}
        )

    @staticmethod
    def get_group_avg_feel_interval(group_name: str, interval: str = None, week_start: str = 'monday') -> dict:
        """
        Retrieve the average feel statistic for all group members during a certain interval in time.
        :param group_name: A name which uniquely identifies a group.
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
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND status='accepted'
                ''',
                {'group_name': group_name}
            )
        else:
            return db.session.execute(
                '''
                SELECT AVG(feel) AS average 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND date >= :date
                AND status='accepted'
                ''',
                {'group_name': group_name, 'date': date}
            )

    @staticmethod
    def get_log_feed(limit: int, offset: int) -> list:
        """
        Retrieve a collection of logs
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :return: A list of logs
        """
        return db.session.execute(
            '''
            SELECT * FROM logs 
            ORDER BY date DESC, log_id DESC
            LIMIT :limit OFFSET :offset
            ''',
            {'limit': limit, 'offset': offset}
        )

    @staticmethod
    def get_user_log_feed(username: str, limit: int, offset: int) -> list:
        """
        Retrieve a collection of logs by a user
        :param username: The unique username for a user
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :return: A list of logs
        """
        return db.session.execute(
            '''
            SELECT * FROM logs 
            WHERE username=:username
            ORDER BY date DESC, log_id DESC
            LIMIT :limit OFFSET :offset
            ''',
            {'username': username, 'limit': limit, 'offset': offset}
        )

    @staticmethod
    def get_group_log_feed(group_name: str, limit: int, offset: int) -> list:
        """
        Retrieve a collection of logs by a group
        :param group_name: The unique name of a group
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :return: A list of logs
        """
        return db.session.execute(
            '''
            SELECT log_id,logs.username,first,last,name,location,date,type,
                    distance,metric,miles,time,pace,feel,description 
            FROM logs 
            INNER JOIN groupmembers ON logs.username=groupmembers.username 
            WHERE group_name=:group_name 
            AND status='accepted' 
            ORDER BY date DESC, log_id DESC 
            LIMIT :limit OFFSET :offset
            ''',
            {'group_name': group_name, 'limit': limit, 'offset': offset}
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
