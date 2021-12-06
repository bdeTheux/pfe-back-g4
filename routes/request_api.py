from flask import jsonify, abort, request, Blueprint

from db.couchDB_service import DatabaseService

REQUEST_API = Blueprint('request_api', __name__)

db = DatabaseService()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/', methods=['GET'])
def get():
    return jsonify({'hello': 'world'})


@REQUEST_API.route('/couch/<string:_doc>', methods=['GET'])
def get_couch(_doc):
    return jsonify(db.get_document(_doc))


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
