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
    filter_values = {
        "r": ["run"],
        "b": ["bike"],
        "s": ["swim"],
        "o": [
            "other",
            "core",
            "strength",
            "weights",
            "yoga",
            "walk",
            "hike",
            "virtual bike",
            "kayak",
            "canoe",
            "row",
            "stand up paddle",
            "alpine ski",
            "backcountry ski",
            "nordic ski",
            "snowboard",
            "snowshoe",
            "ice skate",
            "roller ski",
            "inline skate",
        ],
    }

    return [
        e
        for exercise in [
            filter_values.get(exercise_type, []) for exercise_type in exercise_types
        ]
        for e in exercise
    ]


def generate_exercise_filter_sql_query(filters: list) -> str:
    """
    Generate a MySQL query that filters logs by certain exercise types.
    :param filters: A list of exercise types to filter logs on.
    :return: A SQL query string.
    """
    if filters is None or len(filters) == 0:
        return ""

    sql_query = "type IN ("
    for exercise_filter in filters:
        sql_query += f"'{exercise_filter}'" + ","
    return sql_query[:-1] + ")"
