"""
Activation code routes in the SaintsXCTF API.  Used for retrieving, creating, and deleting codes used
to activate a user account.
Author: Andrew Jarombek
Date: 8/5/2019
"""

from flask import Blueprint, request, jsonify, current_app

activation_code_route = Blueprint('activation_code_route', __name__, url_prefix='/v2/activationcode')


@activation_code_route.route('/', methods=['GET', 'POST'])
def activation_code():
    if request.method == 'GET':
        ''' [GET] /v2/activationcode '''
        pass
    elif request.method == 'POST':
        ''' [POST] /v2/activationcode '''
        pass


@activation_code_route.route('/<code>', methods=['DELETE'])
def activation_code_by_code(code):
    if request.method == 'DELETE':
        ''' [GET] /v2/activationcode/<code> '''
        pass
