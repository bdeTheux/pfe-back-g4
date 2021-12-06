import argparse
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from routes import request_api
import dotenv

app = Flask(__name__)

app.register_blueprint(request_api.get_blueprint())


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


envFile = dotenv.dotenv_values("../.env")
port = envFile.get("port")
print(envFile.get("port"))
print(__name__)

# a tester et comprendre?
if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(app)
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print("test")
        app.run(host='0.0.0.0', port=port, debug=False)
