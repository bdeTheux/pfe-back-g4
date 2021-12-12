from flask import jsonify, abort, request, Blueprint

import services.categories_service as service
from utils.utils import admin_token_required

categories_route = Blueprint('categories-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return categories_route


@categories_route.route('/', methods=['GET'])
def get_all():
    return jsonify(service.get_categories())


@categories_route.route('/tree', methods=['GET'])
def get_organized():
    return jsonify(service.get_categories_as_tree())


@categories_route.route('/<string:_id>', methods=['GET'])
def get_one(_id):
    try:
        category = service.get_category_by_id(_id)
    except AttributeError as e:
        abort(404, e)
    return jsonify(category.get_data())


@categories_route.route('/<string:_id>/subcategories', methods=['GET'])
def get_subcategories(_id):
    return jsonify(service.get_sub_categories(_id))


@categories_route.route('/<string:_id>/parents', methods=['GET'])
def get_parents(_id):
    try:
        parents = service.get_parents(_id)
    except AttributeError as e:
        abort(404, e)
    return jsonify(parents)


@categories_route.route('/', methods=['POST'])
@admin_token_required
def create_one(_current_user):
    if not request.json:
        abort(400, "The payload is empty")
    data = request.json
    name = data.get('name')

    if not name:  # Empty data
        abort(400, "The field 'name' should be there and should not be empty")

    parent = data.get('parent', None)
    sub_categories = data.get('sub_categories') if isinstance(data['sub_categories'], list) else []

    try:
        res = service.create_category(name, parent, sub_categories)
    except AttributeError as e:
        abort(400, e)
    return jsonify(res)


@categories_route.route('/<string:_id>', methods=['DELETE'])
@admin_token_required
def delete_one(_current_user, _id):
    try:
        res = service.delete_category(_id)
    except AttributeError as e:
        abort(404, e)
    return jsonify(res)


@categories_route.route('/<string:_id>', methods=['PUT'])
@admin_token_required
def edit_one(_current_user, _id):
    if not request.json:
        abort(400, "The payload is empty")

    data = request.json
    name = data.get('name')
    parent = data.get('parent', None)
    sub_categories = data.get('sub_categories', [])

    if not name:  # Empty data
        abort(400, "The payload need a field 'name' and it should not be empty")
    if not isinstance(sub_categories, list):
        abort(400, "The payload field 'sub_categories' should be a list")

    try:
        res = service.edit_category(_id, name, parent, sub_categories)
    except AttributeError as e:
        abort(400, e)

    return jsonify(res)
