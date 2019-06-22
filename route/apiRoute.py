"""
Global routes in the SaintsXCTF API.  Used for retrieving information about the API.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from flask import Blueprint, jsonify
from app import version_number

api_route = Blueprint('api_route', __name__, url_prefix='/')


@api_route.route('/', methods=['GET'])
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


@api_route.errorhandler(404)
def error_404(ex):
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'error_description': "Page Not Found",
        'error_code': 404,
        'exception': str(ex)
    }), 404


@api_route.errorhandler(500)
def error_500(ex):
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'error_description': "Internal Server Error",
        'error_code': 500,
        'exception': str(ex)
    }), 500


@api_route.route(f'/v{version_number}/', methods=['GET'])
def version():
    return jsonify({
        'api': 'saints-xctf',
        'version': 2.0,
        'message': f'This endpoint is for version {version_number} of the API.  This is the latest version'
    })