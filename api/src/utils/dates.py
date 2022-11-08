"""
Manage dates with the help of the datetime module.
Author: Andrew Jarombek
Date: 7/4/2019
"""

from typing import Literal, Optional
from datetime import datetime, timedelta, date


Interval = Literal["year", "month", "week"]
WeekStart = Literal["monday", "sunday"]


def get_start_date_interval(
    interval: Optional[Interval], week_start: WeekStart
) -> date:
    """
    Get the start date of a time interval, whether it be the past week, year, or month.
    :param interval: A string representing the interval (week, month, or year).
    :param week_start: Day of the week that is used to signify the start of the week.
    :return: The first date of the time interval.  None if no interval is passed as an argument.
    """
    start_date = None
    if interval == "year":
        start_date = get_first_day_of_year()
    elif interval == "month":
        start_date = get_first_day_of_month()
    elif interval == "week":
        start_date = get_first_day_of_week(week_start=week_start)
    return start_date


def get_first_day_of_year() -> date:
    """
    Retrieve the first day of this year.
    :return: Date object representing January 1st of this year.
    """
    return datetime.today().date().replace(month=1, day=1)


def get_first_day_of_month() -> date:
    """
    Retrieve the first day of this month.
    :return: A Date object.
    """
    return datetime.today().date().replace(day=1)


def get_first_day_of_week(week_start: WeekStart = "monday") -> date:
    """
    Retreive either last Sunday or Monday
    :param week_start: Either 'monday' or 'sunday'
    :return: A date object representing the first day of the past week
    """
    sunday_week_start = 0
    if week_start == "sunday":
        sunday_week_start = 1

    todays_weekday = datetime.now().date().weekday()
    first_day_of_week = datetime.today() - timedelta(
        days=todays_weekday + sunday_week_start
    )
    return first_day_of_week.date()
