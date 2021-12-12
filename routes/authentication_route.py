# flask imports

from flask import request, make_response, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash

import services.users_service as service
from models.User import User
from utils.utils import create_response_with_token

authentication_route = Blueprint('authentication_route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return authentication_route


# route for logging user in
@authentication_route.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json

    if not auth or not auth['email'] or not auth['password']:
        # returns 401 if any email or / and password is missing
        return abort(401, 'Wrong credentials')

    user = service.get_user_by_email(auth['email'])

    if not user:
        # returns 401 if user does not exist
        return abort(401, 'Wrong credentials')

    if check_password_hash(user['password'], auth['password']):
        # generates the JWT Token
        return create_response_with_token(user)
    # returns 403 if password is wrong
    return abort(401, 'Wrong credentials')


# signup route
@authentication_route.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json
    # gets info
    email = data['email']
    password = data['password']

    # checking for existing user
    user = service.get_user_by_email(email)
    if not user:
        # database ORM object
        first_name = data['first_name']
        last_name = data['last_name']
        campus = data['campus']
        user = User(first_name=first_name,
                    last_name=last_name,
                    campus=campus,
                    email=email,
                    password=generate_password_hash(password)
                    )
        # insert user
        service.create_user(user)
        return create_response_with_token(user, 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
