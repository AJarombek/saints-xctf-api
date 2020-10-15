"""
Flask environment configuration for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/23/2019
"""


class LocalConfig:
    ENV = 'local'
    AUTH_URL = 'https://dev.auth.saintsxctf.com'


class TestConfig:
    ENV = 'test'
    # AUTH_URL = 'http://saints-xctf-auth'
    AUTH_URL = 'http://saints-xctf-auth:5000'


class DevelopmentConfig:
    ENV = 'dev'
    AUTH_URL = 'https://dev.auth.saintsxctf.com'


class ProductionConfig:
    ENV = 'prod'
    AUTH_URL = 'https://auth.saintsxctf.com'


config = {
    'local': LocalConfig,
    'test': TestConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
