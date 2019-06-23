"""
Flask environment configuration for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/23/2019
"""


class LocalConfig:
    ENV = 'local'
    BASE_URL = 'localhost:8080'


class DevelopmentConfig:
    ENV = 'dev'
    BASE_URL = 'https://dev.api.saintsxctf.com'


class ProductionConfig:
    ENV = 'prod'
    BASE_URL = 'https://api.saintsxctf.com'


config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
