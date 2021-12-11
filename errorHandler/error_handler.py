from flask import jsonify, make_response


def generic_http_handler(_error):
    return make_response(jsonify({'code': _error.code, 'description': _error.description}), _error.code)
