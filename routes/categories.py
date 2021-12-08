import flask
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
    category = db.get_category_by_id(_id)
    return jsonify(category.get_data()) if category else flask.abort(404)


@categories_route.route('/', methods=['POST'])
def create_one():
    if not request.get_json():
        abort(400, "The payload is empty")

    data = request.get_json(force=True)
    if 'name' not in data:
        abort(400, "The payload need a field 'name'")
    return jsonify(db.create_category(data))


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
