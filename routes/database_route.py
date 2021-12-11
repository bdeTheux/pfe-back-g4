from flask import jsonify, Blueprint

from db import database

database = database.get_database()

database_route = Blueprint('database-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return database_route


@database_route.route('/documents', methods=['GET'])
def get_documents():
    documents = []
    for doc in database:
        documents.append(database[doc])

    return jsonify(documents)
