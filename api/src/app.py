"""
Entry point to the SaintsXCTF API.  The API uses the flask library.
Author: Andrew Jarombek
Date: 6/8/2019
"""

import os
from flask import Flask
from flask_sqlalchemy import get_debug_queries, current_app
from database import db
from bcrypt import bcrypt
from config import config
from utils.db import get_connection_url
from route.activationCodeRoute import activation_code_route
from route.apiRoute import api_route
from route.mailRoute import mail_route
from route.userRoute import user_route
from route.forgotPasswordRoute import forgot_password_route
from route.flairRoute import flair_route
from route.logRoute import log_route
from route.logFeedRoute import log_feed_route
from route.messageRoute import message_route
from route.groupRoute import group_route
from route.commentRoute import comment_route
from route.messageFeedRoute import message_feed_route
from route.rangeViewRoute import range_view_route


def create_app(config_name) -> Flask:
    """
    Application factory function for the Flask app.
    Source: http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    """
    application = Flask(__name__)
    application.config.from_object(config[config_name])

    application.register_blueprint(activation_code_route)
    application.register_blueprint(api_route)
    application.register_blueprint(mail_route)
    application.register_blueprint(user_route)
    application.register_blueprint(forgot_password_route)
    application.register_blueprint(flair_route)
    application.register_blueprint(log_route)
    application.register_blueprint(log_feed_route)
    application.register_blueprint(group_route)
    application.register_blueprint(message_route)
    application.register_blueprint(comment_route)
    application.register_blueprint(message_feed_route)
    application.register_blueprint(range_view_route)

    application.config['SQLALCHEMY_DATABASE_URI'] = get_connection_url()
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_RECORD_QUERIES'] = True
    application.config['SLOW_DB_QUERY_TIME'] = 0.5

    db.init_app(application)
    bcrypt.init_app(application)

    return application


flask_env = os.getenv('FLASK_ENV') or 'local'
app = create_app(flask_env)


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
