# flask imports
import re

from flask import request, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash

import services.users_service as service
from models.User import User
from utils.utils import create_response_with_token

authentication_route = Blueprint('authentication_route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return authentication_route


# route for logging user in
@authentication_route.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json

    if not auth or not auth['email'] or not auth['password']:
        # returns 401 if any email or / and password is missing
        return abort(401, 'Email ou mot de passe incorrect(s)')

    user = service.get_user_by_email(auth['email'])

    if not user:
        # returns 401 if user does not exist
        return abort(401, 'Email ou mot de passe incorrect(s)')

    if check_password_hash(user['password'], auth['password']):
        # generates the JWT Token
        return create_response_with_token(user)
    # returns 403 if password is wrong
    return abort(401, 'Email ou mot de passe incorrect(s)')


# signup route
@authentication_route.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json
    # gets info
    email = data['email']
    password = data['password']

    if not re.match("^\w+\.\w+@(student\.vinci\.be|vinci\.be)$", email):
        return abort(422, "L\'email doit être sous la forme prenom.nom@student.vinci.be ou prenom.nom@vinci.be")
    # checking for existing user
    user = service.get_user_by_email(email)
    if not user:
        # database ORM object
        first_name = data['first_name']
        last_name = data['last_name']
        campus = data['campus']
        user = User(first_name=first_name,
                    last_name=last_name,
                    campus=campus,
                    email=email,
                    password=generate_password_hash(password)
                    )
        # insert user
        user_id = service.create_user(user)
        user = service.get_user_by_id(user_id)
        return create_response_with_token(user, 201)
    else:
        return abort(409, 'L\'utilisateur existe déjà : Connectez-vous.')
