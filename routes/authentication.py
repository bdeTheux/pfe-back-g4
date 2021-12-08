# flask imports
from datetime import datetime, timedelta
from functools import wraps

import dotenv
import jwt
from flask import request, jsonify, make_response, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash

import db.couchDB_service as db
from models.User import User

envFile = dotenv.dotenv_values(".env")  # might cause problem so add ../
# JWT info
JWT_NAME = envFile.get("JWTName")
SECRET_KEY = envFile.get("JWTSecret")
authentication_route = Blueprint('authentication_route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return authentication_route


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if JWT_NAME in request.headers:
            token = request.headers[JWT_NAME]
        # return 401 if token is not passed
        if not token:
            return abort(401, 'Token is missing !!')

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=[
                "HS256"])  # TODO -> signature has expired quand on lance la même requête 2h later ?
            current_user = db.get_user_by_id(data['public_id'])
        except Exception as e:
            print(e)
            return abort(401, 'Token is invalid !!')
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if JWT_NAME in request.headers:
            token = request.headers[JWT_NAME]
        # return 401 if token is not passed
        if not token:
            return abort(401, 'Token is missing !!')

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=[
                "HS256"])  # TODO -> signature has expired quand on lance la même requête 2h later ?
            current_user = db.get_user_by_id(data['public_id'])
        except Exception as e:
            print(e)
            return abort(401, 'Token is invalid !!')
        if not current_user.is_admin:
            return abort(401, 'Admin only!!')
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# route for logging user in
@authentication_route.route('/login/', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json
    print(auth)
    if not auth or not auth['email'] or not auth['password']:
        # returns 401 if any email or / and password is missing
        return abort(401, 'Could not verify1')  # make_response(
        # 'Could not verify',
        # 401,
        # {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        # )

    user = db.get_user_by_email(auth['email'])

    if not user:
        # returns 401 if user does not exist
        return abort(401, 'Could not verify2')  # make_response(
        # 'Could not verify',
        # 401,
        # {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        # )

    if check_password_hash(user['password'], auth['password']):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(minutes=120),
            'algorithm': "HS256"
        }, SECRET_KEY)
        resp = make_response(jsonify({'token': token}))  # throw/throw http error au lieu de make_response
        resp.headers[JWT_NAME] = token
        return resp  # throw/throw http error au lieu de make_response
    # returns 403 if password is wrong
    return abort(403, 'Could not verify3')  # make_response(
    # 'Could not verify',
    # 403,
    # {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    # )


# signup route
@authentication_route.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json
    print(data)
    # gets info
    email = data['email']
    password = data['password']

    # checking for existing user
    user = db.get_user_by_email(email)
    print(user)
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
        db.create_user(user)
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
