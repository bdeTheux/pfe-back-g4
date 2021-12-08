from flask import jsonify, make_response


def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': _error.description}), 400)


def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': _error.description}), 401)


def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': _error.description}), 404)


def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': _error.description}), 500)
