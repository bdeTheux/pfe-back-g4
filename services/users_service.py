import uuid

from db import database
from models.User import User

database = database.get_database()


def create_user(user):
    user_id = uuid.uuid4().hex
    database[user_id] = dict(type='User', last_name=user.last_name,
                             first_name=user.first_name, email=user.email,
                             password=user.password, campus=user.campus, is_banned=False,
                             is_admin=False)
    return user_id


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
    return previous_user.get_limited_data()


def ban_user(_id):
    user = get_user_by_id(_id)
    user['is_banned'] = not user['is_banned']
    user.store(database)
    return user.get_data()
