import flask
from flask import jsonify, abort, request, Blueprint
from werkzeug.security import generate_password_hash

import db.couchDB_service as db
from models.User import User
from routes.authentication import token_required

users_route = Blueprint('users-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_route


# done
@users_route.route('/', methods=['GET'])
@token_required
def get_all(current_user):
    return jsonify(db.get_users()) if current_user['is_admin'] \
        else flask.abort(401)


# Done
@users_route.route('/<string:_id>', methods=['GET'])
@token_required
def get_with_id(current_user, _id):
    user = db.get_user_by_id(_id)
    if user:
        return jsonify(user.to_admin()) if current_user['is_admin'] \
            else jsonify(user.to_public())
    else:
        return flask.abort(404)


# done
@users_route.route('/<string:_id>/ban', methods=['POST'])
@token_required
def ban(current_user, _id):
    if not current_user['is_admin']:
        flask.abort(401)

    return jsonify(db.ban_user(_id))


# done
@users_route.route('/<string:_id>', methods=['DELETE'])
@token_required
def delete_one(current_user, _id):
    return jsonify(db.delete_user(_id)) if current_user['is_admin'] \
        else flask.abort(401)


# done
@users_route.route('/<string:_id>', methods=['PUT'])
@token_required
def edit_one(current_user, _id):
    if current_user['_id'] != _id:
        abort(401)

    data = request.form
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
    return jsonify(db.edit_user(user, _id))
