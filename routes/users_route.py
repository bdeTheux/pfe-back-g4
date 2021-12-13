import flask
from flask import jsonify, abort, request, Blueprint
from werkzeug.security import generate_password_hash

import services.users_service as service
from models.User import User
from utils.utils import token_required, token_welcome, admin_token_required

users_route = Blueprint('users-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_route


@users_route.route('/', methods=['GET'])
@admin_token_required
def get_all(_current_user):
    return jsonify(service.get_users())


@users_route.route('/whoami', methods=['GET'])
@token_welcome
def whoami(_current_user: User):
    return jsonify(_current_user.get_data()) if _current_user else jsonify(None)


@users_route.route('/<string:_id>', methods=['GET'])
@token_required
def get_with_id(current_user, _id):
    user = service.get_user_by_id(_id)
    if user:
        return jsonify(user.get_data()) if current_user['is_admin'] \
            else jsonify(user.get_limited_data())
    else:
        return flask.abort(404)


@users_route.route('/<string:_id>/ban', methods=['POST'])
@admin_token_required
def ban(_current_user, _id):
    return jsonify(service.ban_user(_id))


@users_route.route('/<string:_id>', methods=['DELETE'])
@admin_token_required
def delete_one(_current_user, _id):
    return jsonify(service.delete_user(_id))


@users_route.route('/<string:_id>', methods=['PUT'])
@token_required
def edit_one(current_user, _id):
    if current_user['_id'] != _id:
        abort(401, 'Vous n\'avez pas accès à cette fonctionnalité.')

    data = request.json
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    campus = data.get('campus')
    password = data.get('password')
    user = User(_id=_id,
                first_name=first_name,
                last_name=last_name,
                campus=campus,
                email=email,
                password=generate_password_hash(password)
                )
    return jsonify(service.edit_user(user, _id))
