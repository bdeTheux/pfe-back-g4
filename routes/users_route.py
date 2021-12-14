import flask
from flask import jsonify, abort, request, Blueprint
from werkzeug.security import generate_password_hash

import services.users_service as service
from models.User import User
from services.posts_service import get_post_by_id
from utils.utils import token_required, token_welcome, admin_token_required, check_password

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


@users_route.route('/edit', methods=['PUT'])
@token_required
def edit_one(current_user):
    if not request.json:
        abort(400, "La requête est vide")

    data = request.json
    email = data.get('email', current_user['email'])
    first_name = data.get('first_name', current_user['email'])
    last_name = data.get('last_name', current_user['last_name'])
    campus = data.get('campus', current_user['campus'])
    password = data.get('password', current_user['password'])
    user = User(_id=current_user['_id'],
                first_name=first_name,
                last_name=last_name,
                campus=campus,
                email=email,
                password=generate_password_hash(password)
                )
    return jsonify(service.edit_user(user, current_user['_id']))


@users_route.route('/changepassword', methods=['POST'])
@token_required
def change_password(_current_user):
    if not request.json:
        abort(400, "La requête est vide")
    data = request.json
    current_password = data.get('current_password')

    check_password(_current_user['password'], current_password)

    new_password = generate_password_hash(data.get('new_password'))
    return jsonify(service.change_password(_current_user['_id'], new_password))


@users_route.route('/changefavorite/<string:_id>', methods=['POST'])
@token_required
def change_favorite(current_user, _id):  # id post
    post = get_post_by_id(_id)
    if not post:
        abort(404, "Cette annonce n'existe pas/plus.")

    return jsonify(service.change_favorite(current_user['_id'], _id))
