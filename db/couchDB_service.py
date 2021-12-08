import os
import uuid

import couchdb
import dotenv

from models.Category import Category
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
    mango = {
        'selector': {'type': 'Category'},
        'fields': ['name', 'parent', 'sub_categories']
    }
    return list(database.find(mango))


def get_category_by_id(_id):
    return Category.load(database, _id)


def create_category(_data):
    """Create a new category only if the same name does not exist already.
    Parameters
        _data: a dict containing at lease the key 'name', and optionally 'parent' and 'sub_categories'
            - the 'parent' has to exist already in the DB, or it will be set to None.
            - the 'sub_categories' has to be a list of strings. If the categories in the list does not exist,
              they are created as sub_categories of the new one. If they exist, they are ignored.
    Returns
        The name (and id) of the added category
    """
    if 'parent' in _data and Category.load(database, _data['parent']):
        parent = _data['parent']
    else:
        parent = None

    sub_categories = []
    if 'sub_categories' in _data:
        for cat in _data['sub_categories']:
            existing_cat = Category.load(database, cat)
            if not existing_cat:
                database[cat] = dict(type='Category', name=cat, parent=_data['name'],
                                     sub_categories=[])
                sub_categories.append(cat)

    database[_data['name']] = dict(type='Category', name=_data['name'], parent=parent, sub_categories=sub_categories)

    return _data['name']


def delete_category(_id):
    category = Category.load(database, _id)

    if not category:
        raise FileNotFoundError

    if category.parent:
        parent = Category.load(database, category.parent)
        parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
        parent.store(database)
    for cat in category.sub_categories:  # TODO recursive func
        try:
            database.delete(Category.load(database, cat))
        except TypeError:  # It should not happen but it does not matter either
            pass
    return database.delete(category)


def edit_category(_id, _data):
    """Edit a category by its given id.
    Parameters
        _data: a dict containing 3 key 'name', 'parent', and 'sub_categories'
            - the 'parent' has to either exist in the DB or to be null.
              if it is not null and does not exist, it is aborted
            - the 'sub_categories' has to be a list of strings.
              If it does not have the same items as the original in the DB, the operation is aborted.
              If it has additional items with parents, it is aborted.
              If it has additional unknown items, they are created.
    Returns
        The name (and id) of the added category
    """
    print(_data)
    category = Category.load(database, _id)
    if not category:
        raise AttributeError
    # If sub_categories are missing, aborting
    missing_subs = set(category.sub_categories).difference(_data['sub_categories'])
    if len(missing_subs) != 0:
        raise AttributeError

    # If new sub_categories already have a parent, aborting
    new_subs = set(_data['sub_categories']).difference(category.sub_categories)
    for cat in new_subs:
        c = Category.load(database, cat)
        if c and c.parent:
            raise AttributeError

    if category.parent != _data['parent']:
        if _data['parent']:
            parent = Category.load(database, category.parent)
            if not parent:
                raise AttributeError
            parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
            parent.store(database)

        category.parent = _data['parent']

    for cat in new_subs:
        c = Category.load(database, cat)
        if c:
            c.parent = category.name
            c.store(database)
        else:
            create_category({"name": c})
            
    return _data['name']


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


def get_user_by_id(_id):
    return User.load(database, _id)


def get_user_by_public_id(_public_id):
    return None


def get_user_by_email(_email):
    mango = {
        'selector': {'type': 'User', 'email': _email}
    }
    if len(list(database.find(mango))):
        return list(database.find(mango))[0]
    return list(database.find(mango))[0] if len(list(database.find(mango))) > 0 else None


def get_users():
    mango = {
        'selector': {'type': 'User'}
    }
    return list(database.find(mango))


def delete_user(_id):
    return None


def edit_user():
    return None


def ban_user(data):
    if not data:
        print("ban definitif")
    # ban selon data
    return None
