import couchdb
import dotenv

envfile = dotenv.dotenv_values(".env")

username = envfile.get("DBDevUsername")
password = envfile.get("DBDevPassword")
host = envfile.get("DBDevHost")

server = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))
database = server["pfe-df-g4"]
documents = database.get("_all_docs")


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
def create_user():
    return None


def get_user_by_id(_id):
    return None


def get_users():
    return None


def delete_user(_id):
    return None


def edit_user():
    return None


def ban_user(data):
    if not data:
        print("ban definitif")
    # ban selon data
    return None
