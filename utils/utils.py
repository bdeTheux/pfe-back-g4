import os
from datetime import datetime, timedelta
from functools import wraps

import cloudinary
import dotenv
import jwt
from cloudinary import uploader
from cloudinary import uploader
from flask import make_response, request, abort, jsonify
from werkzeug.security import check_password_hash

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
    FOLDER = "PFE_dev"
else:
    JWT_NAME = os.environ["JWTName"]
    SECRET_KEY = os.environ["JWTSecret"]
    FOLDER = "PFE_prod"


def _get_user_from_token(token):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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
            return abort(401, 'Token manquant')

        try:
            current_user = _get_user_from_token(token)
        except Exception:
            return abort(401, 'Token invalide')
        if not current_user:
            abort(401, 'Token invalide')
        if current_user['is_banned']:
            abort(401, 'Vous êtes banni!')
        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        if not token:
            return abort(401, 'Token manquant')

        try:
            current_user = _get_user_from_token(token)
        except Exception:
            return abort(401, 'Token invalide')
        if not current_user:
            abort(401, 'Token invalide')
        if not current_user.is_admin:
            return abort(401, 'Accès administrateur uniquement')
        if current_user['is_banned']:
            abort(401, 'Vous êtes banni!')
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


def upload_images(images):
    upload_result = []
    for image in images:
        print(image)
        upload_result.append(uploader.upload(image))
    return upload_result


def check_password(current, given):
    if not check_password_hash(current, given):
        return abort(401, 'Mot de passe incorrect.')


def upload_files(files) -> (list[str], str):
    images = []
    video = None
    for file_to_upload in files:
        try:
            if file_to_upload:
                if "video" in file_to_upload.content_type and not video:  # One video only, no matter what
                    # videos are set at 25% of quality to be lighter only. Test should be made with the max
                    video = cloudinary.uploader.upload(file_to_upload, folder=FOLDER, resource_type="video",
                                                       quality="25").get('url')
                elif "image" in file_to_upload.content_type:
                    images.append(cloudinary.uploader.upload(file_to_upload, folder=FOLDER).get('url'))
        except Exception as e:
            print("error", e)  # Just ignoring problems since there is a wide range of them and little time
        pass

    return images, video


def remove_file(_file_id: str):
    # TODO images are found but not videos, same path and everything...?
    if _file_id == "accessories-bag":  # Generic image
        AttributeError("Vous ne pouvez pas supprimer l'image par défaut")
    return cloudinary.uploader.destroy(f'{FOLDER}/{_file_id}')
