"""
Generate filters for retrieving exercise data.
Author: Andrew Jarombek
Date: 8/5/2019
"""


def create_exercise_filter_list(exercise_types: str) -> list:
    """
    Take a string of characters and convert them into a list of exercise types.
    :param exercise_types: String of characters which are initials for exercise types.
    :return: A list of strings representing exercise types.
    """
    return [char_to_exercise(exercise_type) for exercise_type in exercise_types]


def char_to_exercise(exercise_type: str) -> str:
    """
    Convert a character to its corresponding exercise type.
    :param exercise_type: A character representing an exercise type.
    :return: A string representing an exercise type.
    """
    if exercise_type == 'r':
        return 'run'
    elif exercise_type == 'b':
        return 'bike'
    elif exercise_type == 's':
        return 'swim'
    elif exercise_type == 'o':
        return 'other'
    else:
        return 'other'


def generate_exercise_filter_sql_query(filters: list) -> str:
    """
    Generate a MySQL query that filters logs by certain exercise types.
    :param filters: A list of exercise types to filter logs on.
    :return: A SQL query string.
    """
    if filters is None or filters.__len__() == 0:
        return ''
    else:
        sql_query = 'type IN ('
        for exercise_filter in filters:
            sql_query += exercise_filter + ','
        return sql_query[:-1] + ')'
