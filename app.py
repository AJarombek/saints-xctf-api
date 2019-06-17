"""
Entry point to the SaintsXCTF API.  The API uses the flask library.
Author: Andrew Jarombek
Date: 6/8/2019
"""

from flask import Flask, jsonify
from route.mailRoute import mail_route

version_number = 2


def create_app():
    """
    Application factory function for the Flask app.
    Source: http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    """
    app = Flask(__name__)
    app.register_blueprint(mail_route)


@app.route('/', methods=['GET'])
def api():
    """
    Entry point for the SaintsXCTF API
    :return: A JSON welcome message
    """
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'message': 'Welcome to the saints-xctf API!'
    })


@app.errorhandler(404)
def error_404(ex):
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'error_description': "Page Not Found",
        'error_code': 404,
        'exception': str(ex)
    }), 404


@app.errorhandler(500)
def error_500(ex):
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'error_description': "Internal Server Error",
        'error_code': 500,
        'exception': str(ex)
    }), 500


@app.route(f'/v{version_number}/', methods=['GET'])
def version():
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'message': f'This endpoint is for version {version_number} of the API.  This is the latest version'
    })


if __name__ == '__main__':
    app.run(port=8081)
