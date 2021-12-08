import flask
from flask import jsonify, abort, request, Blueprint

import db.couchDB_service as db
from routes.authentication import admin_token_required

categories_route = Blueprint('categories-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return categories_route


@categories_route.route('/', methods=['GET'])
def get_all():
    return jsonify(db.get_categories())


@categories_route.route('/<string:_id>', methods=['GET'])
def get_one(_id):
    category = db.get_category_by_id(_id)
    return jsonify(category.get_data()) if category else flask.abort(404)


@categories_route.route('/', methods=['POST'])
@admin_token_required
def create_one(current_user):
    if not request.get_json():
        abort(400, "The payload is empty")

    data = request.get_json(force=True)

    if 'name' not in data:  # No data
        abort(400, "The payload need a field 'name'")
    if not data['name']:  # Empty data
        abort(400, "The field 'name' should not be empty")
    if db.get_category_by_id(data['name']):
        abort(400, "The category exists already")
    res = db.create_category(data)
    return jsonify(res) if res else abort(400, "Something wrong happened")


@categories_route.route('/<string:_id>', methods=['DELETE'])
@admin_token_required
def delete_one(current_user, _id):
    try:
        res = db.delete_category(_id)
    except FileNotFoundError:
        abort(404, "Category not found")
    return jsonify(res)


@categories_route.route('/<string:_id>', methods=['PUT'])
@admin_token_required
def edit_one(_current_user, _id):
    if not request.get_json():
        abort(400, "The payload is empty")

    data = request.get_json(force=True)
    if 'name' not in data:
        abort(400, "The payload need a field 'name'")
    if 'parent' not in data:
        abort(400, "The payload need a field 'parent'")
    if 'sub_categories' not in data:
        abort(400, "The payload need a field 'sub_categories'")
    return jsonify(db.edit_category(_id, data))
