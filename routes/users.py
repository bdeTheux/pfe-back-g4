from flask import jsonify, abort, request, Blueprint

import db.couchDB_service as db

users_route = Blueprint('users-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_route


@users_route.route('/', methods=['GET'])
def get_all():
    return jsonify(db.get_users())


@users_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    # code ...
    return db.get_user_by_id(_id)


@users_route.route('/<string:_id>/ban', methods=['POST'])
def ban(_id):
    if not request.get_json():
        return jsonify(db.ban_user(None))

    data = request.get_json(force=True)

    return jsonify(db.ban_user(data))


@users_route.route('/', methods=['POST'])
def create_one():
    if not request.get_json():
        abort(400)

    # data = request.get_json(force=True)

    return jsonify(db.create_user())


@users_route.route('/<string:_id>', methods=['DELETE'])
def delete_one(_id):
    # code ...
    return jsonify(db.delete_user(_id))


@users_route.route('/<string:_id>', methods=['PUT'])
def edit_one(_id):
    if not request.get_json():
        abort(400)

    # data = request.get_json(force=True)

    return jsonify(db.edit_user())
