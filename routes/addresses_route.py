from flask import jsonify, abort, request, Blueprint

import services.addresses_service as service
from utils.utils import admin_token_required

addresses_route = Blueprint('addresses-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return addresses_route


@addresses_route.route('/', methods=['GET'])
def get_all():
    return jsonify(service.get_addresses())


@addresses_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    res = service.get_address_by_id(_id)
    return jsonify(res) if res else abort(404, 'Référence invalide')


@addresses_route.route('/', methods=['POST'])
@admin_token_required
def create_one(_current_user):
    if not request.json:
        abort(400, "La requête est vide")

    data = request.json
    campus = data.get('campus', None)
    lat = data.get('lat', None)
    long = data.get('long', None)
    if not campus:
        abort(400, "La requête nécessite un champ 'campus' non vide")
    if not lat:
        abort(400, "La requête nécessite un champ 'lat' non vide")
    if not long:
        abort(400, "La requête nécessite un champ 'long' non vide")

    try:
        res = service.create_address(campus, lat, long)
    except AttributeError as e:
        abort(400, e)
    return jsonify(res)


@addresses_route.route('/<string:_id>', methods=['DELETE'])
@admin_token_required
def delete_one(_current_user, _id):
    try:
        res = service.delete_address(_id)
    except AttributeError as e:
        abort(400, e)
    return jsonify(res)


@addresses_route.route('/<string:_id>', methods=['PUT'])
@admin_token_required
def edit_one(_current_user, _id):
    if not request.json:
        abort(400, "The payload is empty")

    data = request.json
    campus = data.get('campus', None)
    lat = data.get('lat', None)
    long = data.get('long', None)
    if not campus:
        abort(400, "La requête nécessite un champ 'campus' non vide")
    if not lat:
        abort(400, "La requête nécessite un champ 'lat' non vide")
    if not long:
        abort(400, "La requête nécessite un champ 'long' non vide")

    try:
        res = service.edit_address(_id, campus, lat, long)
    except AttributeError as e:
        abort(400, e)

    return jsonify(res)
