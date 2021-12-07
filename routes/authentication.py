# flask imports
import uuid  # for public id
from datetime import datetime, timedelta
from functools import wraps

import dotenv
import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

import db.couchDB_service as db
from app.main import app
from models.User import User

envFile = dotenv.dotenv_values("/.env")  # might cause problem so add ../
print(envFile)

# JWT info
JWT_NAME = envFile.get("JWTName")
SECRET_KEY = envFile.get("JWTSecret")


# Database ORMs


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.get_user_by_public_id(data['public_id'])
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = db.get_user_by_email(auth.get('email'))

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets info
    email = data.get('email')
    password = data.get('password')

    # checking for existing user
    user = db.get_user_by_email(email)
    if not user:
        # database ORM object
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        campus = data.get('campus')
        user = User(public_id=str(uuid.uuid4()),
                    first_name=first_name,
                    last_name=last_name,
                    campus=campus,
                    email=email,
                    password=generate_password_hash(password)
                    )
        # insert user
        db.create_user(user)
        # db.session.commit() -> ????
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
