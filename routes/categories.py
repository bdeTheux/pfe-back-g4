from flask import jsonify, abort, request, Blueprint

import db.couchDB_service as db

categories_route = Blueprint('categories-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return categories_route


@categories_route.route('/', methods=['GET'])
def get():
    return jsonify(db.get_categories())


@categories_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    # code ...
    return jsonify(db.get_category_by_id(_id))


@categories_route.route('/', methods=['POST'])
def get_request():
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(db.create_category())


@categories_route.route('/<string:_id>', methods=['DELETE'])
def delete(_id):
    # code ...
    return jsonify(db.delete_category(_id))


@categories_route.route('/<string:_id>', methods=['PUT'])
def edit_one(_id):
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(db.edit_category())
