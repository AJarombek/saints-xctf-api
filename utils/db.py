"""
Database Connection to MySQL for use by the API
Author: Andrew Jarombek
Date: 6/12/2019
"""

import os
from pymysql import connect, cursors, Connection
from utils import aws


def get_connection() -> Connection:
    """
    Connect to the MySQL database depending on the environment
    :return: Connection object for interacting with the MySQL database
    """
    try:
        env = os.environ['ENV']
    except KeyError:
        env = "prod"

    secret_map = aws.retrieve_db_cred(env)
    db_host = aws.retrieve_db_host(env)

    return connect(
        host=db_host,
        user=secret_map.get("username"),
        password=secret_map.get("password"),
        db='saintsxctf',
        charset='utf8mb4',
        cursorclass=cursors.DictCursor
    )
