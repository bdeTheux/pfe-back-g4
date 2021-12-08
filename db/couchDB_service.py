import os
import uuid

import couchdb
import dotenv

from models.User import User

envfile = dotenv.dotenv_values(".env")
try:
    environment = os.environ["FLASK_ENV"]
except Exception:
    environment = "prod"
if environment == "development":
    username = envfile.get("DBDevUsername")
    password = envfile.get("DBDevPassword")
    host = envfile.get("DBDevHost")
else:
    username = os.environ["DBProdUsername"]
    password = os.environ["DBProdPassword"]
    host = os.environ["DBProdHost"]

server = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))

database = server["pfe-df-g4"]

documents = database.get("_all_docs")


# # database['kevinnnn'] = dict(type='User', name='Kevin Jullien', campus='woluwe')
#
# mango = {
#     'selector': {'type': 'User'},
#     'fields': ['name', 'campus']
# }
#
# for row in database.find(mango):
#     print(row['name'], row['campus'])


def get_document(_document):
    print(database, _document)
    return database.get


# Addresses
def get_addresses():
    return None


def get_address_by_id(_id):
    return None


def create_address():
    return None


def delete_address(_id):
    return None


def edit_address():
    return None


# Categories
def get_categories():
    return {
        "categorie1": "truc",
        "categorie2": "machin"
    }


def get_category_by_id(_id):
    return {
        "categorie1": "truc"
    }


def create_category():
    return None


def delete_category(_id):
    return None


def edit_category():
    return None


# Posts
def get_posts():
    return None


def get_post_by_id(_id):
    return None


def create_post():
    return None


def delete_post(_id):
    return None


def edit_post():
    return None


def get_pending_posts():
    return None


def get_post_by_campus_and_category(campus, category):
    return None


def get_post_by_campus(campus):
    return None


def get_post_by_category(category):
    return None


# Users

def create_user(user):
    database[uuid.uuid4().hex] = dict(type='User', last_name=user.last_name,
                                      first_name=user.first_name, email=user.email,
                                      password=user.password, campus=user.campus, is_banned=False,
                                      is_admin=False)


# DONE
def get_user_by_id(_id):
    return User.load(database, _id)


# DONE
def get_user_by_email(_email):
    mango = {
        'selector': {'type': 'User', 'email': _email}
    }
    if len(list(database.find(mango))):
        return list(database.find(mango))[0]
    return list(database.find(mango))[0] if len(list(database.find(mango))) > 0 else None


# DONE
def get_users():
    mango = {
        'selector': {'type': 'User'}
    }
    return list(database.find(mango))


def delete_user(_id):
    user = get_user_by_id(_id)
    database.delete(user)
    return None


def edit_user():
    return None


def ban_user(data):
    if not data:
        print("ban definitif")
    # ban selon data
    return None
