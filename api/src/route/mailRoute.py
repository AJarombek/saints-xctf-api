"""
Mail routes in the SaintsXCTF API.  Used for sending emails.
Author: Andrew Jarombek
Date: 6/14/2019
"""

from flask import Blueprint

mail_route = Blueprint('mail_route', __name__, url_prefix='/mail')


@mail_route.route('/', methods=['POST'])
def mail():
    pass
