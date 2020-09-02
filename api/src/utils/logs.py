"""
Helper functions for managing and creating exercise logs.
Author: Andrew Jarombek
Date: 9/1/2020
"""

import re


def to_miles(metric: str, distance: float) -> float:
    """
    Function to convert a distance of a certain unit to miles.
    :param metric: The unit of measurement used.
    :param distance: The distance in the specified unit of measurement.
    :return: The distance converted to miles
    """
    if metric == 'miles':
        return distance
    elif metric == 'meters':
        return distance / 1609.344
    elif metric == 'kilometers':
        return distance * 0.621317
    else:
        return distance


def calculate_mile_pace(miles: float, time: str) -> str:
    """
    Calculate the mile pace of an exercise.
    :param miles: The length of the exercise in miles.
    :param time: The time taken exercising (represented as a string).
    :return: The pace per mile of the exercise (represented as a string).
    """
    hour_regex = re.compile(r'(\d{1,2}):(\d{2}):(\d{2})')
    minute_regex = re.compile(r'(\d{1,2}):(\d{2})')
    seconds_regex = re.compile(r'(\d{2})')

    hour = 0
    minute = 0
    second = 0

    if match := hour_regex.fullmatch(time):
        hour, minute, second = match.group(1, 2, 3)
    elif match := minute_regex.fullmatch(time):
        minute, second = match.group(1, 2)
    elif match := seconds_regex.fullmatch(time):
        second = match.group(1)

    total_seconds = (int(hour) * 60 * 60) + (int(minute) * 60) + int(second)
    second_pace = total_seconds / miles

    second_str = str(second_pace % 60)
    minute_str = str((second_pace // 60) % 60)
    hour_str = str((second_pace // 3600))

    if len(second_str) == 1:
        second_str = f'0{second_str}'

    if len(minute_str) == 1:
        minute_str = f'0{minute_str}'

    if len(hour_str) == 1:
        hour_str = f'0{hour_str}'

    return f'{hour_str}:{minute_str}:{second_str}'
