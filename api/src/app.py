"""
Entry point to the SaintsXCTF API.  The API uses the flask library.
Author: Andrew Jarombek
Date: 6/8/2019
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, get_debug_queries, current_app
from flask.ext.bcrypt import Bcrypt
from config import config
from utils.db import get_connection_url
from route.apiRoute import api_route
from route.mailRoute import mail_route
from route.userRoute import user_route

version_number = 2

db = SQLAlchemy()


def create_app(config_name) -> Flask:
    """
    Application factory function for the Flask app.
    Source: http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(api_route)
    app.register_blueprint(mail_route)
    app.register_blueprint(user_route)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    app.config['SLOW_DB_QUERY_TIME'] = 0.5

    config[config_name].init_app(app)
    db.init_app(app)

    return app


flask_env = os.getenv('FLASK_ENV') or 'local'
app = create_app(flask_env)

bcrypt = Bcrypt(app)


@app.after_request
def after_request(response):
    """
    Actions to perform after each request to the API.  Keep track of slow database queries
    and log them as warnings to the console/log file.
    :param response: HTTP response object.
    :return: Propagate the HTTP response object
    """
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context)
            )
    return response
