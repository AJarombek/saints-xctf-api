"""
Activation code routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting codes used
to activate a user account.
Author: Andrew Jarombek
Date: 8/5/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.activationCodeDao import ActivationCodeDao
from model.Code import Code

activation_code_route = Blueprint('activation_code_route', __name__, url_prefix='/v2/activation_code')


@activation_code_route.route('/', methods=['POST'])
def activation_code():
    """
    Endpoint for creating new activation codes.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'POST':
        ''' [POST] /v2/activation_code '''
        return activation_code_post()


@activation_code_route.route('/<code>', methods=['GET', 'DELETE'])
def activation_code_by_code(code):
    """
    Endpoints for retrieving a single activation codes and deleting codes.
    :param code: Random characters that make up an activation code.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/activation_code/<code> '''
        return activation_code_by_code_get(code)

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/activation_code/<code> '''
        return activation_code_by_code_delete(code)


@activation_code_route.route('/links', methods=['GET'])
def activation_code_links():
    """
    Endpoint for information about the activation code API endpoints.
    :return: Metadata about the activation code API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/activation_code/links '''
        return activation_code_links_get()


def activation_code_post():
    code_data: dict = request.get_json()
    code_to_add = Code(code_data)
    code_added_successfully = ActivationCodeDao.add_activation_code(new_code=code_to_add)

    if code_added_successfully:
        code_added = ActivationCodeDao.get_activation_code(code=code_to_add.activation_code)

        response = jsonify({
            'self': '/v2/activation_code',
            'added': True,
            'activation_code': code_added
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': '/v2/activation_code',
            'added': False,
            'activation_code': None,
            'error': 'failed to create a new activation code'
        })
        response.status_code = 500
        return response


def activation_code_by_code_get(code: str):
    matching_codes = ActivationCodeDao.activation_code_exists(code)
    matching_code_exists = matching_codes.get('exists')

    if matching_code_exists:
        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'matching_code_exists': matching_code_exists,
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'matching_code_exists': matching_code_exists,
            'error': 'there is no matching activation code'
        })
        response.status_code = 400
        return response


def activation_code_by_code_delete(code: str):
    is_deleted = ActivationCodeDao.delete_code(activation_code=code)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'deleted': False,
            'error': 'failed to delete the activation code'
        })
        response.status_code = 500
        return response


def activation_code_links_get():
    response = jsonify({
        'self': f'/v2/activation_code/links',
        'endpoints': [
            {
                'link': '/v2/activation_code',
                'verb': 'POST',
                'description': 'Create a new activation code.'
            },
            {
                'link': '/v2/activation_code/<code>',
                'verb': 'GET',
                'description': 'Retrieve a single activation code with a given unique code.'
            },
            {
                'link': '/v2/activation_code/<code>',
                'verb': 'DELETE',
                'description': 'Delete a single activation code.'
            }
        ],
    })
    response.status_code = 200
    return response