"""
Activation code routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting codes used
to activate a user account.
Author: Andrew Jarombek
Date: 8/5/2019
"""

from flask import Blueprint, request, jsonify, current_app
from dao.activationCodeDao import ActivationCodeDao
from model.Code import Code

activation_code_route = Blueprint('activation_code_route', __name__, url_prefix='/v2/activationcode')


@activation_code_route.route('/', methods=['GET', 'POST'])
def activation_code():
    """
    Endpoint for creating new activation codes.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'POST':
        ''' [POST] /v2/activationcode '''
        code_data: dict = request.get_json()
        code_to_add = Code(code_data)
        code_added_successfully = ActivationCodeDao.add_activation_code(new_code=code_to_add)

        if code_added_successfully:
            pass
        else:
            pass


@activation_code_route.route('/<code>', methods=['DELETE'])
def activation_code_by_code(code):
    """
    Endpoints for retrieving a single activation codes and deleting codes.
    :param code: Random characters that make up an activation code.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/activationcode '''
        matching_codes = ActivationCodeDao.activation_code_exists(code)
        matching_code_exists = matching_codes.get('exists')

        if matching_code_exists:
            response = jsonify({
                'self': f'/v2/activationcode/{code}',
                'matching_code_exists': matching_code_exists,
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'self': f'/v2/activationcode/{code}',
                'matching_code_exists': matching_code_exists,
                'error': 'there is no matching activation code'
            })
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        ''' [DELETE] /v2/activationcode/<code> '''
        pass
