"""
Database Connection to MySQL for use by the API
Author: Andrew Jarombek
Date: 6/12/2019
"""

import os
from utils import aws


def get_connection_url() -> str:
    """
    Create a connection URL to the MySQL database depending on the environment
    :return: Connection URL for interacting with the MySQL database
    """
    try:
        env = os.environ['ENV']
    except KeyError:
        env = "prod"

    # Local development credentials aren't stored in a Secret
    if env == 'local':
        return 'mysql+pymysql://saintsxctflocal:saintsxctf@db/saintsxctf'

    secret_map = aws.retrieve_db_cred(env)

    hostname = aws.retrieve_db_host(env)
    username = secret_map.get("username")
    password = secret_map.get("password")
    database = 'saintsxctf'

    return f'mysql+pymysql://{username}:{password}@{hostname}/{database}'
