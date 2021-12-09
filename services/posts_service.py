import uuid

from db import database
from models.Post import Post

database = database.get_database()


def get_document(_document):
    print(database, _document)
    return database.get


def get_posts():
    mango = {
        'selector': {'type': 'Post'},
    }
    return list(database.find(mango))


def get_posts_by_campus(campus):
    mango = {
        'selector': {'type': 'Post'}
    }
    list_posts = [row for row in list(database.find(mango)) if campus in row['address_id']]
    return list_posts


def get_posts_by_category(category):
    mango = {
        'selector': {'type': 'Post',
                     'category_id': category},
    }
    return list(database.find(mango))


def get_pending_posts():
    mango = {
        'selector': {'type': 'Post', 'state': 'Pending'},
    }
    return list(database.find(mango))


def get_post_by_id(_id):
    return Post.load(database, _id)


def create_post(post):
    id_post = uuid.uuid4().hex
    database[id_post] = dict(type='Post', post_nature=post.post_nature, state="Pending", title=post.title,
                             description=post.description, address_id=post.address_id,
                             seller_id=post.seller_id, category_id=post.category_id)
    return id_post


def delete_post(_id):
    post = get_post_by_id(_id)
    return database.delete(post)


def edit_post(new_post, _id):
    previous_post = get_post_by_id(_id)
    new_post['_id'] = _id
    new_post['state'] = new_post['state']
    new_post['category_id'] = previous_post['category_id']
    new_post['seller_id'] = previous_post['seller_id']

    for field in new_post:
        previous_post[field] = new_post[field]
    previous_post.store(database)
    return previous_post.get_data()


def get_posts_by_campus_and_category(campus, category):
    mango = {
        'selector': {'type': 'Post',
                     'category_id': category}
    }
    list_posts = [row for row in list(database.find(mango)) if campus in row['address_id']]
    return list_posts


def change_state(_id, state):
    post = get_post_by_id(_id)
    post['state'] = state
    post.store(database)
    return post.get_data()
