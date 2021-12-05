from flask import jsonify, abort, request, Blueprint

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/', methods=['GET'])
def get():
    return jsonify({'hello': 'world'})


@REQUEST_API.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    # code ...
    return jsonify(_id)


@REQUEST_API.route('/request', methods=['POST'])
def get_request():
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    return jsonify(data)
