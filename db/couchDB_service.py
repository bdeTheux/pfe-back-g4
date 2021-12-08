import uuid

from db import database
from models.Category import Category
from models.User import User

database = database.get_database()


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
    parent_category = None
    if 'parent' in _data and (parent_category := Category.load(database, _data['parent'])):
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

    if parent_category:
        parent_category.sub_categories.append(_data['name'])
        parent_category.store(database)

    return _data['name']


def delete_category(_id):
    """Delete a category and its sub-categories."""
    category = Category.load(database, _id)

    if not category:
        raise FileNotFoundError

    if category.parent:
        parent = Category.load(database, category.parent)
        parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
        parent.store(database)

    return delete_category_and_sub_categories(category)


def delete_category_and_sub_categories(node: Category):
    if not node:
        return
    for child in node.sub_categories:
        cat = Category.load(database, child)
        delete_category_and_sub_categories(cat)
    database.delete(node)
    return True


def edit_category(_id, _data):
    """Edit a category by its given id and the given data.
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



# Users


def create_user(user):
    database[uuid.uuid4().hex] = dict(type='User', last_name=user.last_name,
                                      first_name=user.first_name, email=user.email,
                                      password=user.password, campus=user.campus, is_banned=False,
                                      is_admin=False)


def get_user_by_id(_id):
    return User.load(database, _id)


def get_user_by_email(_email):
    mango = {
        'selector': {'type': 'User', 'email': _email}
    }
    if len(list(database.find(mango))):
        return list(database.find(mango))[0]
    return list(database.find(mango))[0] if len(list(database.find(mango))) > 0 else None


def get_users():
    mango = {
        'selector': {'type': 'User'},
        'fields': ['_id', 'last_name', 'first_name', 'email', 'campus', 'is_admin', 'is_banned']
    }
    return list(database.find(mango))


# Delete tous ses posts ?
def delete_user(_id):
    user = get_user_by_id(_id)
    return database.delete(user)


def edit_user(new_user, _id):
    """This function edits a user already in the database,
    Parameters
        _new_user: a User object containing everything but the is_admin or is_banned fields
        -_id: the id of the user who its fields need to be modified
    Returns
        The user (with its public fields) with the updated fields
    """

    new_user['_id'] = _id
    previous_user = get_user_by_id(_id)
    for field in new_user:
        previous_user[field] = new_user[field]
    previous_user.store(database)
    return previous_user.to_public()


def ban_user(_id):
    user = get_user_by_id(_id)
    user['is_banned'] = not user['is_banned']
    user.store(database)
    return user.to_admin()
