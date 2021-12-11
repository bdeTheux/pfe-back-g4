# flask imports
import os
from datetime import datetime, timedelta
from functools import wraps

import dotenv
import jwt
from flask import request, make_response, Blueprint, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import services.users_service as service
from models.User import User

envfile = dotenv.dotenv_values(".env")
# JWT info
try:
    environment = os.environ["FLASK_ENV"]
except Exception:
    environment = "prod"
if environment == "development":
    JWT_NAME = envfile.get("JWTName")
    SECRET_KEY = envfile.get("JWTSecret")
else:
    JWT_NAME = os.environ["JWTName"]
    SECRET_KEY = os.environ["JWTSecret"]

authentication_route = Blueprint('authentication_route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return authentication_route


def _get_user_from_token(token):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # TODO -> signature has expired quand on lance la même requête 2h later ?
    current_user = service.get_user_by_id(data['public_id'])
    return current_user


def _get_token():
    token = None
    if JWT_NAME in request.headers:
        token = request.headers[JWT_NAME]
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        if not token:
            return abort(401, 'Token is missing !!')

        try:
            current_user = _get_user_from_token(token)
        except Exception:
            return abort(401, 'Token is invalid !!')
        if not current_user:
            abort(401, 'Token is invalid !!')
        # TODO: bloquer si profil banni
        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        if not token:
            return abort(401, 'Token is missing !!')

        try:
            current_user = _get_user_from_token(token)
        except Exception:
            return abort(401, 'Token is invalid !!')
        if not current_user:
            abort(401, 'Token is invalid !!')
        if not current_user.is_admin:
            return abort(401, 'Admin only!!')
        return f(current_user, *args, **kwargs)

    return decorated


def token_welcome(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()

        try:
            current_user = _get_user_from_token(token)
        except Exception:
            current_user = None

        return f(current_user, *args, **kwargs)

    return decorated


# route for logging user in
@authentication_route.route('/login/', methods=['POST'])
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
        token = jwt.encode({
            'public_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(minutes=120),
            'algorithm': "HS256"
        }, SECRET_KEY)
        resp = make_response(jsonify({'token': token}))
        resp.headers[JWT_NAME] = token
        return resp
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
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
