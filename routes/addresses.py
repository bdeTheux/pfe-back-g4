from flask import jsonify, abort, request, Blueprint

import services.addresses_service as service

addresses_route = Blueprint('addresses-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return addresses_route


@addresses_route.route('/', methods=['GET'])
def get_all():
    return jsonify(service.get_addresses())


@addresses_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    # code ...
    return jsonify(service.get_address_by_id(_id))


@addresses_route.route('/', methods=['POST'])
def post_request():
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(service.create_address())


@addresses_route.route('/<string:_id>', methods=['DELETE'])
def delete(_id):
    # code ...
    return jsonify(service.delete_address(_id))


@addresses_route.route('/<string:_id>', methods=['PUT'])
def edit_one(_id):
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(service.edit_address())
