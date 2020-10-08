"""
Flask environment configuration for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/23/2019
"""


class LocalConfig:
    ENV = 'local'
    BASE_URL = 'localhost:8080'
    AUTH_URL = 'https://dev.auth.saintsxctf.com'


class DevelopmentConfig:
    ENV = 'dev'
    BASE_URL = 'https://dev.api.saintsxctf.com'
    AUTH_URL = 'https://dev.auth.saintsxctf.com'


class ProductionConfig:
    ENV = 'prod'
    BASE_URL = 'https://api.saintsxctf.com'
    AUTH_URL = 'https://auth.saintsxctf.com'


config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
