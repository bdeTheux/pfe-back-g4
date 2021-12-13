from flask import jsonify, Blueprint

from db import database
from db.couchDB_functions import init_database, display_db_docs

database = database.get_database()

database_route = Blueprint('database-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return database_route


@database_route.route('/documents', methods=['GET'])
def get_documents():
    return jsonify(display_db_docs(database))


@database_route.route('/init', methods=['GET'])
def reinit_database():
    init_database(database)
    return jsonify(display_db_docs(database))
