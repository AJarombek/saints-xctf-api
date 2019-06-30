"""
Global routes in the SaintsXCTF API.  Used for retrieving information about the API.
Author: Andrew Jarombek
Date: 6/21/2019
"""

from flask import Blueprint, jsonify

api_route = Blueprint('api_route', __name__, url_prefix='/')


@api_route.route('/', methods=['GET'])
def api():
    """
    Entry point for the SaintsXCTF API
    :return: A JSON welcome message
    """
    return jsonify({
        'self_link': '/',
        'api_name': 'saints-xctf-api',
        'versions_link': '/versions'
    })


@api_route.route('/versions', methods=['GET'])
def versions():
    return jsonify({
        'self': '/versions',
        'version_latest': '/v2',
        'version_1': None,
        'version_2': '/v2'
    })


@api_route.route('/v2', methods=['GET'])
def version2():
    return jsonify({
        'self': '/v2',
        'version': 2,
        'latest': True,
        'entities': '/v2/entities'
    })


@api_route.route('/v2/entities', methods=['GET'])
def entities():
    return jsonify({
        'self': '/v2/entities',
        'admin': '/v2/mail',
        'code': '/v2/users'
    })


@api_route.errorhandler(404)
def error_404(ex):
    return jsonify({
        'error_description': "Page Not Found",
        'exception': str(ex),
        'contact': 'andrew@jarombek.com',
        'api_index': '/versions'
    }), 404


@api_route.errorhandler(500)
def error_500(ex):
    return jsonify({
        'error_description': "Internal Server Error",
        'exception': str(ex),
        'contact': 'andrew@jarombek.com'
    }), 500
