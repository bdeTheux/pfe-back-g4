import os
from datetime import datetime, timedelta
from functools import wraps

import dotenv
import jwt
from flask import make_response, request, abort, jsonify

import services.users_service as service
from models.User import User

envfile = dotenv.dotenv_values(".env")

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


def create_token(user):
    return jwt.encode({
        'public_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(days=30),
        'algorithm': "HS256"
    }, SECRET_KEY)


def create_response_with_token(user: User, code=200):
    token = create_token(user)
    resp = make_response(jsonify({'token': token}), code)
    resp.headers[JWT_NAME] = token
    return resp


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
