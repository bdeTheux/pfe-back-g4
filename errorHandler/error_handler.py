from flask import jsonify, make_response


def generic_http_handler(_error):
    return make_response(jsonify({'error': _error.description}), _error.code)
