"""
Manage dates with the help of the datetime module.
Author: Andrew Jarombek
Date: 7/4/2019
"""

from datetime import datetime, timedelta


def get_first_day_of_year():
    return datetime.today().date().replace(month=1, day=1)


def get_first_day_of_month():
    return datetime.today().date().replace(day=1)


def get_first_day_of_week(week_start: str = 'monday'):

    sunday_week_start = 0
    if week_start == 'sunday':
        sunday_week_start = 1

    todays_weekday = datetime.now().date().weekday()
    first_day_of_week = datetime.today() - timedelta(days=todays_weekday + sunday_week_start)
    return first_day_of_week.date()
