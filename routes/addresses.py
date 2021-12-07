from flask import jsonify, abort, request, Blueprint

import db.couchDB_service as db

addresses_route = Blueprint('addresses-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return addresses_route


@addresses_route.route('/', methods=['GET'])
def get_all():
    return jsonify(db.get_addresses())


@addresses_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    # code ...
    return jsonify(db.get_address_by_id(_id))


@addresses_route.route('/', methods=['POST'])
def post_request():
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(db.create_address())


@addresses_route.route('/<string:_id>', methods=['DELETE'])
def delete(_id):
    # code ...
    return jsonify(db.delete_address(_id))


@addresses_route.route('/<string:_id>', methods=['PUT'])
def edit_one(_id):
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(db.edit_address())
