"""
Retrieve credentials from AWS SecretsManager
Author: Andrew Jarombek
Date: 6/12/2019
"""

import boto3
import json


def retrieve_db_cred(env: str = 'prod') -> map:
    """
    Retrieve the username and password for the database running in a given environment.
    :param env: The environment the API is running in.
    :return: A dictionary containing a username and password.
    """
    secretsmanager = boto3.client('secretsmanager')
    response = secretsmanager.get_secret_value(SecretId=f'saints-xctf-rds-{env}-secret')
    secret_string = response.get("SecretString")
    secret_dict = json.loads(secret_string)

    return {"username": secret_dict.get("username"), "password": secret_dict.get("password")}


def retrieve_db_host(env: str = 'prod') -> str:
    """
    Retrieve the hostname for the database running in a given environment.
    :param env: The environment the API is running in.
    :return: A string representing the database hostname.
    """
    rds = boto3.client('rds')
    rds_instances = rds.describe_db_instances(DBInstanceIdentifier=f'saints-xctf-mysql-database-{env}')
    instance = rds_instances.get('DBInstances')[0]
    return instance.get('Endpoint').get('Address')
