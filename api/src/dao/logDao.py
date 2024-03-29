"""
Log data access from the SaintsXCTF MySQL database.  Contains exercise logs for users.
Author: Andrew Jarombek
Date: 7/3/2019
"""

from typing import Optional

from sqlalchemy.engine.cursor import ResultProxy
from sqlalchemy.engine.row import Row

from dao.basicDao import BasicDao
from database import db
from model.Log import Log
from utils import dates
from utils.literals import WeekStart
from utils.exerciseFilters import generate_exercise_filter_sql_query


class LogDao:
    @staticmethod
    def get_logs() -> list:
        """
        Retrieve all the exercise logs in the database
        :return: The result of the query.
        """
        return Log.query.filter(Log.deleted.is_(False)).order_by(Log.date).all()

    @staticmethod
    def get_log_by_id(log_id: int) -> Log:
        """
        Retrieve a specific exercise log based on its id number
        :param log_id: Unique identifier for an exercise log.
        :return: The result of the query.
        """
        return Log.query.filter_by(log_id=log_id).filter(Log.deleted.is_(False)).first()

    @staticmethod
    def get_user_miles(username: str) -> Optional[Row]:
        """
        Get the total exercise miles for a user
        :param username: Unique identifier for a user
        :return: The total number of miles exercised
        """
        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {"username": username},
        )
        return result.first()

    @staticmethod
    def get_user_miles_by_type(username: str, exercise_type: str) -> Optional[Row]:
        """
        Get the total miles of a certain exercise for a user
        :param username: Unique identifier for a user
        :param exercise_type: A certain type of exercise
        :return: The total number of miles exercised of a certain type
        """
        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT SUM(miles) AS total 
            FROM logs 
            WHERE username=:username
            AND type=:exercise_type
            AND deleted IS FALSE
            """,
            {"username": username, "exercise_type": exercise_type},
        )
        return result.first()

    @staticmethod
    def get_user_miles_interval(
        username: str, interval: str = None, week_start: WeekStart = "monday"
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                AND deleted IS FALSE
                """,
                {"username": username},
            )
        else:
            result: ResultProxy = db.session.execute(  # pylint: disable=no-member
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND date >= :date
                AND deleted IS FALSE
                """,
                {"username": username, "date": date},
            )

        return result.first()

    @staticmethod
    def get_user_miles_interval_by_type(
        username: str,
        exercise_type: str,
        interval: str = None,
        week_start: WeekStart = "monday",
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username
                AND type=:exercise_type
                AND deleted IS FALSE
                """,
                {"username": username, "exercise_type": exercise_type},
            )
        else:
            result: ResultProxy = db.session.execute(  # pylint: disable=no-member
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                WHERE username=:username 
                AND type=:exercise_type
                AND date >= :date
                AND deleted IS FALSE
                """,
                {"username": username, "date": date, "exercise_type": exercise_type},
            )

        return result.first()

    @staticmethod
    def get_user_avg_feel(username: str) -> Optional[Row]:
        """
        Retrieve the average feel statistic for a user
        :param username: Unique identifier for a user
        :return: The average feel
        """
        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT AVG(feel) AS average 
            FROM logs 
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {"username": username},
        )
        return result.first()

    @staticmethod
    def get_user_avg_feel_interval(
        username: str, interval: str = None, week_start: WeekStart = "monday"
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                AND deleted IS FALSE
                """,
                {"username": username},
            )
        else:
            result: ResultProxy = db.session.execute(  # pylint: disable=no-member
                """
                SELECT AVG(feel) AS average 
                FROM logs 
                WHERE username=:username
                AND date >= :date
                AND deleted IS FALSE
                """,
                {"username": username, "date": date},
            )

        return result.first()

    @staticmethod
    def get_group_miles(group_name: str) -> Optional[Row]:
        """
        Get the total exercise miles for all the users in a group.
        :param group_name: Unique name for a group.
        :return: The total number of miles exercised.
        """
        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT SUM(miles) AS total 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_name": group_name},
        )
        return result.first()

    @staticmethod
    def get_group_miles_interval(
        group_name: str, interval: str = None, week_start: WeekStart = "monday"
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name
                AND status='accepted'
                AND logs.deleted IS FALSE
                AND groupmembers.deleted IS FALSE
                """,
                {"group_name": group_name},
            )
            return result.first()

        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT SUM(miles) AS total 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND date >= :date 
            AND status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_name": group_name, "date": date},
        )
        return result.first()

    @staticmethod
    def get_group_miles_interval_by_type(
        group_name: str,
        exercise_type: str,
        interval: str = None,
        week_start: WeekStart = "monday",
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT SUM(miles) AS total 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND type=:exercise_type
                AND status='accepted'
                AND logs.deleted IS FALSE
                AND groupmembers.deleted IS FALSE
                """,
                {"group_name": group_name, "exercise_type": exercise_type},
            )
            return result.first()

        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT SUM(miles) AS total 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND type=:exercise_type
            AND date >= :date 
            AND status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {
                "group_name": group_name,
                "exercise_type": exercise_type,
                "date": date,
            },
        )
        return result.first()

    @staticmethod
    def get_group_avg_feel(group_name: str) -> Optional[Row]:
        """
        Retrieve the average feel statistic for a group.
        :param group_name: A name which uniquely identifies a group.
        :return: The average feel.
        """
        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT AVG(feel) AS average 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_name": group_name},
        )
        return result.first()

    @staticmethod
    def get_group_avg_feel_interval(
        group_name: str, interval: str = None, week_start: WeekStart = "monday"
    ) -> Optional[Row]:
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
            # pylint: disable=no-member
            result: ResultProxy = db.session.execute(
                """
                SELECT AVG(feel) AS average 
                FROM logs 
                INNER JOIN groupmembers ON logs.username = groupmembers.username 
                WHERE group_name=:group_name 
                AND status='accepted'
                AND logs.deleted IS FALSE
                AND groupmembers.deleted IS FALSE
                """,
                {"group_name": group_name},
            )
            return result.first()

        # pylint: disable=no-member
        result: ResultProxy = db.session.execute(
            """
            SELECT AVG(feel) AS average 
            FROM logs 
            INNER JOIN groupmembers ON logs.username = groupmembers.username 
            WHERE group_name=:group_name 
            AND date >= :date
            AND status='accepted'
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_name": group_name, "date": date},
        )
        return result.first()

    @staticmethod
    def get_log_feed(limit: int, offset: int, username: str) -> ResultProxy:
        """
        Retrieve a collection of logs.  The logs returned depend upon which teams the user making the
        request is a member of.
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :param username: Unique identifier of the user making the log feed request
        :return: A list of logs
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT DISTINCT logs.* FROM logs
            INNER JOIN teammembers
            ON logs.username = teammembers.username
            WHERE teammembers.deleted IS FALSE
            AND logs.deleted IS FALSE
            AND teammembers.team_name IN (
                SELECT team_name FROM teammembers
                WHERE username = :username
                AND status = 'accepted'
                AND deleted IS FALSE
            )
            ORDER BY logs.date DESC, log_id DESC
            LIMIT :limit OFFSET :offset
            """,
            {"limit": limit, "offset": offset, "username": username},
        )

    @staticmethod
    def get_log_feed_count() -> ResultProxy:
        """
        Calculate the number of logs in the log feed.
        :return: The number of logs in existence.
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT COUNT(*) AS count FROM logs WHERE deleted IS FALSE
            """
        )

    @staticmethod
    def get_user_log_feed(username: str, limit: int, offset: int) -> ResultProxy:
        """
        Retrieve a collection of logs by a user
        :param username: The unique username for a user
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :return: A list of logs
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT * FROM logs 
            WHERE username=:username
            AND deleted IS FALSE
            ORDER BY date DESC, log_id DESC
            LIMIT :limit OFFSET :offset
            """,
            {"username": username, "limit": limit, "offset": offset},
        )

    @staticmethod
    def get_user_log_feed_count(username: str) -> ResultProxy:
        """
        Calculate the number of logs in a users log collection.
        :param username: The unique username for a user
        :return: The number of logs in existence.
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT COUNT(*) AS count FROM logs
            WHERE username=:username
            AND deleted IS FALSE
            """,
            {"username": username},
        )

    @staticmethod
    def get_group_log_feed(group_id: int, limit: int, offset: int) -> ResultProxy:
        """
        Retrieve a collection of logs by a group
        :param group_id: The unique id of a group
        :param limit: The maximum number of logs to return
        :param offset: The number of logs to skip before returning
        :return: A list of logs
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT log_id,logs.username,first,last,name,location,date,type,
                    distance,metric,miles,time,pace,feel,description 
            FROM logs 
            INNER JOIN groupmembers ON logs.username=groupmembers.username 
            WHERE group_id=:group_id 
            AND status='accepted' 
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            ORDER BY date DESC, log_id DESC 
            LIMIT :limit OFFSET :offset
            """,
            {"group_id": group_id, "limit": limit, "offset": offset},
        )

    @staticmethod
    def get_group_log_feed_count(group_id: int) -> ResultProxy:
        """
        Calculate the number of logs in a groups log collection.
        :param group_id: The unique id of a group
        :return: The number of logs in existence.
        """
        # pylint: disable=no-member
        return db.session.execute(
            """
            SELECT COUNT(*) AS count FROM logs
            INNER JOIN groupmembers ON logs.username=groupmembers.username 
            WHERE group_id=:group_id 
            AND status='accepted' 
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            """,
            {"group_id": group_id},
        )

    @staticmethod
    def get_range_view(types: list, start: str, end: str) -> ResultProxy:
        """
        Get exercise log statistics over a date range.
        :param types: Types of exercise logs to filter by.
        :param start: The first date to include in the range.
        :param end: The last date to include in the range.
        :return: A list of exercise miles and feel statistics for each day a log exists.
        """
        type_query = generate_exercise_filter_sql_query(types)
        # pylint: disable=no-member
        return db.session.execute(
            f"""
            SELECT date, SUM(miles) AS miles, CAST(AVG(feel) AS UNSIGNED) AS feel 
            FROM logs 
            WHERE date >= :start 
            AND date <= :end
            AND deleted IS FALSE
            AND {type_query}
            GROUP BY date
            """,
            {"start": start, "end": end},
        )

    @staticmethod
    def get_user_range_view(
        username: str, types: list, start: str, end: str
    ) -> ResultProxy:
        """
        Get exercise log statistics for a user over a date range.
        :param username: Unique identifier for a user.
        :param types: Types of exercise logs to filter by.
        :param start: The first date to include in the range.
        :param end: The last date to include in the range.
        :return: A list of exercise miles and feel statistics for each day a log exists.
        """
        type_query = generate_exercise_filter_sql_query(types)
        # pylint: disable=no-member
        return db.session.execute(
            f"""
            SELECT date, SUM(miles) AS miles, CAST(AVG(feel) AS UNSIGNED) AS feel 
            FROM logs 
            WHERE username=:username 
            AND deleted IS FALSE
            AND date >= :start 
            AND date <= :end
            AND {type_query}
            GROUP BY date
            """,
            {"username": username, "start": start, "end": end},
        )

    @staticmethod
    def get_group_range_view(
        group_id: int, types: list, start: str, end: str
    ) -> ResultProxy:
        """
        Get exercise log statistics for a group over a date range.
        :param group_id: Unique identifier for a group.
        :param types: Types of exercise logs to filter by.
        :param start: The first date to include in the range.
        :param end: The last date to include in the range.
        :return: A list of exercise miles and feel statistics for each day a log exists.
        """
        type_query = generate_exercise_filter_sql_query(types)
        # pylint: disable=no-member
        return db.session.execute(
            f"""
            SELECT date, SUM(miles) AS miles, CAST(AVG(feel) AS UNSIGNED) AS feel 
            FROM logs 
            INNER JOIN groupmembers 
            ON logs.username=groupmembers.username 
            WHERE group_id=:group_id
            AND logs.deleted IS FALSE
            AND groupmembers.deleted IS FALSE
            AND date >= :start 
            AND date <= :end
            AND {type_query}
            GROUP BY date
            """,
            {"group_id": group_id, "start": start, "end": end},
        )

    @staticmethod
    def add_log(new_log: Log) -> bool:
        """
        Add an exercise log to the database.
        :param new_log: Object representing an exercise log for a user.
        :return: True if the log is inserted into the database, False otherwise.
        """
        # pylint: disable=no-member
        db.session.add(new_log)
        return BasicDao.safe_commit()

    @staticmethod
    def update_log(log: Log) -> bool:
        """
        Update a log in the database.
        :param log: Object representing an updated log.
        :return: True if the log is updated in the database, False otherwise.
        """
        # pylint: disable=no-member
        db.session.execute(
            """
            UPDATE logs SET 
                name=:name, 
                location=:location, 
                date=:date,
                type=:type, 
                distance=:distance, 
                metric=:metric,
                time=:time,
                miles=:miles,
                pace=:pace,
                feel=:feel, 
                description=:description
            WHERE log_id=:log_id
            AND deleted IS FALSE
            """,
            {
                "name": log.name,
                "location": log.location,
                "date": log.date,
                "type": log.type,
                "distance": log.distance,
                "metric": log.metric,
                "time": log.time,
                "miles": log.miles,
                "pace": log.pace,
                "feel": log.feel,
                "description": log.description,
                "log_id": log.log_id,
            },
        )
        return BasicDao.safe_commit()

    @staticmethod
    def delete_log(log_id: int) -> bool:
        """
        Delete a log from the database based on its id.
        :param log_id: ID which uniquely identifies the log.
        :return: True if the deletion was successful without error, False otherwise.
        """
        # pylint: disable=no-member
        db.session.execute(
            "DELETE FROM logs WHERE log_id=:log_id AND deleted IS FALSE",
            {"log_id": log_id},
        )
        return BasicDao.safe_commit()

    @staticmethod
    def soft_delete_log(log: Log) -> bool:
        """
        Soft Delete an exercise log from the database.
        :param log: Object representing a log to soft delete.
        :return: True if the soft deletion was successful without error, False otherwise.
        """
        # pylint: disable=no-member
        db.session.execute(
            """
            UPDATE logs SET 
                deleted=:deleted,
                modified_date=:modified_date,
                modified_app=:modified_app,
                deleted_date=:deleted_date,
                deleted_app=:deleted_app
            WHERE log_id=:log_id
            AND deleted IS FALSE
            """,
            {
                "log_id": log.log_id,
                "deleted": log.deleted,
                "modified_date": log.modified_date,
                "modified_app": log.modified_app,
                "deleted_date": log.deleted_date,
                "deleted_app": log.deleted_app,
            },
        )
        return BasicDao.safe_commit()
