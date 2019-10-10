"""
Activation code routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting codes used
to activate a user account.
Author: Andrew Jarombek
Date: 8/5/2019
"""

from datetime import datetime
from flask import Blueprint, request, jsonify, Response, redirect, url_for
from sqlalchemy.schema import Column
from dao.activationCodeDao import ActivationCodeDao
from model.Code import Code

activation_code_route = Blueprint('activation_code_route', __name__, url_prefix='/v2/activation_code')


@activation_code_route.route('', methods=['POST'])
def activation_code_redirect() -> Response:
    """
    Redirect endpoints looking for a resource named 'activation_code' to the activation code routes.
    :return: Response object letting the browser know where to redirect the request to.
    """
    if request.method == 'POST':
        ''' [POST] /v2/activation_code '''
        return redirect(url_for('activation_code_route.activation_code'), code=307)


@activation_code_route.route('/', methods=['POST'])
def activation_code() -> Response:
    """
    Endpoint for creating new activation codes.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'POST':
        ''' [POST] /v2/activation_code '''
        return activation_code_post()


@activation_code_route.route('/<code>', methods=['GET', 'DELETE'])
def activation_code_by_code(code) -> Response:
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


@activation_code_route.route('/exists/<code>', methods=['GET'])
def activation_code_exists_by_code(code) -> Response:
    """
    Endpoints determining if an activation code exists.
    :param code: Random characters that make up an activation code.
    :return: JSON representation of an activation code and relevant metadata.
    """
    if request.method == 'GET':
        ''' [GET] /v2/activation_code/exists/<code> '''
        return activation_code_exists_get(code)


@activation_code_route.route('/soft/<code>', methods=['DELETE'])
def activation_code_soft_by_code(code) -> Response:
    """
    Endpoints for soft deleting activation codes.
    :param code: Random characters that make up an activation code.
    :return: JSON representation of activation codes and relevant metadata.
    """
    if request.method == 'DELETE':
        ''' [DELETE] /v2/activation_code/soft/<code> '''
        return activation_code_by_code_soft_delete(code)


@activation_code_route.route('/links', methods=['GET'])
def activation_code_links() -> Response:
    """
    Endpoint for information about the activation code API endpoints.
    :return: Metadata about the activation code API.
    """
    if request.method == 'GET':
        ''' [GET] /v2/activation_code/links '''
        return activation_code_links_get()


def activation_code_post() -> Response:
    """
    Create a new activation code.
    :return: A response object for the POST API request
    """
    code_data: dict = request.get_json()

    if code_data is None:
        response = jsonify({
            'self': f'/v2/activation_code',
            'added': False,
            'error': "the request body isn't populated"
        })
        response.status_code = 400
        return response

    code_to_add: Code = Code(code_data)

    # Perform some validation on the JSON object coming from the client.
    if code_to_add.activation_code is None:
        response = jsonify({
            'self': f'/v2/activation_code',
            'added': False,
            'error': "'activation_code' is a required field"
        })
        response.status_code = 400
        return response

    if len(code_to_add.activation_code) != 6 or type(code_to_add.activation_code) is not str:
        response = jsonify({
            'self': f'/v2/activation_code',
            'added': False,
            'error': "'activation_code' must be a string of length 6"
        })
        response.status_code = 400
        return response

    # The created date must be accurate, don't trust the date coming from the client.
    code_to_add.created_date = datetime.now()

    code_added_successfully: bool = ActivationCodeDao.add_activation_code(new_code=code_to_add)

    if code_added_successfully:
        code_added: Code = ActivationCodeDao.get_activation_code(code=code_to_add.activation_code)
        code_added_dict: dict = code_added.__dict__
        del code_added_dict['_sa_instance_state']

        response = jsonify({
            'self': '/v2/activation_code',
            'added': True,
            'activation_code': code_added_dict
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


def activation_code_exists_get(code: str) -> Response:
    """
    Determine if an activation code exists.
    :param code: The unique activation code.
    :return: A response object for the GET API request
    """
    matching_codes: Column = ActivationCodeDao.activation_code_exists(code)
    matching_code_exists: int = matching_codes['exists']

    if matching_code_exists == 1:
        response = jsonify({
            'self': f'/v2/activation_code/exists/{code}',
            'matching_code_exists': matching_code_exists,
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/activation_code/exists/{code}',
            'matching_code_exists': matching_code_exists,
            'error': 'there is no matching activation code'
        })
        response.status_code = 400
        return response


def activation_code_by_code_get(code: str) -> Response:
    """
    Get an activation code based on its unique code.
    :param code: The unique activation code.
    :return: A response object for the GET API request
    """
    activation_code_object: Code = ActivationCodeDao.get_activation_code(code=code)

    if activation_code_object is not None:
        activation_code_dict: dict = activation_code_object.__dict__
        del activation_code_dict['_sa_instance_state']

        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'activation_code': activation_code_dict,
        })
        response.status_code = 200
        return response
    else:
        response = jsonify({
            'self': f'/v2/activation_code/{code}',
            'activation_code': None,
            'error': 'there is no matching activation code'
        })
        response.status_code = 400
        return response


def activation_code_by_code_delete(code: str) -> Response:
    """
    Delete an activation code based on a unique code.
    :param code: The activation code to delete.
    :return: A response object for the DELETE API request.
    """
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


def activation_code_by_code_soft_delete(code: str) -> Response:
    """
    Soft delete an activation code based on a unique code.
    :param code: The activation code to delete.
    :return: A response object for the DELETE API request.
    """
    existing_code: Code = ActivationCodeDao.get_activation_code(code=code)

    if existing_code is None:
        response = jsonify({
            'self': f'/v2/activation_code/soft/{existing_code}',
            'deleted': False,
            'error': 'there is no existing activation code with this code'
        })
        response.status_code = 400
        return response

    # Update the activation code model to reflect the soft delete
    existing_code.deleted = True
    existing_code.deleted_date = datetime.now()
    existing_code.deleted_app = 'api'
    existing_code.modified_date = datetime.now()
    existing_code.modified_app = 'api'

    is_deleted = ActivationCodeDao.soft_delete_code(existing_code)

    if is_deleted:
        response = jsonify({
            'self': f'/v2/activation_code/soft/{code}',
            'deleted': True,
        })
        response.status_code = 204
        return response
    else:
        response = jsonify({
            'self': f'/v2/activation_code/soft/{code}',
            'deleted': False,
            'error': 'failed to soft delete the activation code'
        })
        response.status_code = 500
        return response


def activation_code_links_get() -> Response:
    """
    Get all the other activation code API endpoints.
    :return: A response object for the GET API request
    """
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
            },
            {
                'link': '/v2/activation_code/soft/<code>',
                'verb': 'DELETE',
                'description': 'Soft delete a single activation code.'
            }
        ],
    })
    response.status_code = 200
    return response
