"""
Flask environment configuration for the SaintsXCTF API.
Author: Andrew Jarombek
Date: 6/23/2019
"""


class LocalConfig:
    ENV = 'local'
    AUTH_URL = 'http://saints-xctf-auth:5000'


class LocalTestConfig:
    ENV = 'localtest'
    AUTH_URL = 'http://saints-xctf-auth:5000'


class TestConfig:
    ENV = 'test'
    AUTH_URL = 'http://localhost:5000'


class DevelopmentConfig:
    ENV = 'dev'
    AUTH_URL = 'https://dev.auth.saintsxctf.com'


class ProductionConfig:
    ENV = 'prod'
    AUTH_URL = 'https://auth.saintsxctf.com'


config = {
    'local': LocalConfig,
    'localtest': LocalTestConfig,
    'test': TestConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
