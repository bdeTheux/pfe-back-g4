import uuid

from db import database
from models.Post import Post, PostStates

database = database.get_database()


def get_document(_document):
    print(database, _document)
    return database.get


def _order_posts(posts, order):
    return sorted(posts, key=lambda i: (i['price'])) if order == "asc" \
        else sorted(posts, key=lambda i: (i['price']), reverse=True)


def get_posts(order):
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.APPROVED.value},

    return _order_posts(list(database.find(mango)), order)


def get_posts_by_campus(campus, order):
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.APPROVED.value},
    }
    list_posts = [row for row in list(database.find(mango)) if campus in row['places']]
    return _order_posts(list(database.find(mango)), order)


def get_posts_by_category(category, order):
    mango = {
        'selector': {'type': 'Post',
                     'category_id': category,
                     'state': PostStates.APPROVED.value},
    }
    return _order_posts(list(database.find(mango)), order)


def get_active_posts_by_category(category):
    mango_pending = {
        'selector': {'type': 'Post',
                     'category_id': category,
                     'state': PostStates.PENDING.value}
    }
    mango_approved = {
        'selector': {'type': 'Post',
                     'category_id': category,
                     'state': PostStates.APPROVED.value}
    }
    posts = list(database.find(mango_pending))
    posts.extend(list(database.find(mango_approved)))
    return posts


def get_pending_posts():
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.PENDING.value},
    }
    return list(database.find(mango))


def get_rejected_posts():
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.REJECTED.value},
    }
    return list(database.find(mango))


def get_post_by_id(_id):
    return Post.load(database, _id)


def create_post(post):
    id_post = uuid.uuid4().hex
    database[id_post] = dict(type='Post', post_nature=post.post_nature, state=PostStates.PENDING.value,
                             title=post.title, price=post.price,
                             description=post.description, places=post.places,
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


def get_posts_by_campus_and_category(campus, categories, order):
    list_posts = []
    for category in categories:
        mango = {
            'selector': {'type': 'Post',
                         'category_id': category,
                         'state': PostStates.APPROVED.value},
        }
        list_posts.extend([row for row in list(database.find(mango)) if campus in row['places']])
    return _order_posts(list_posts, order)


def change_state(_id, state):
    post = get_post_by_id(_id)
    post['state'] = state
    post.store(database)
    return post.get_data()


def get_all_my_posts(_id):
    mango = {
        'selector': {'type': 'Post',
                     'seller_id': _id}
    }
    my_posts = list(database.find(mango))
    my_sorted_posts = {PostStates.APPROVED.value: [x for x in my_posts if x['state'] == PostStates.APPROVED.value],
                       PostStates.PENDING.value: [x for x in my_posts if x['state'] == PostStates.PENDING.value],
                       PostStates.CLOSED.value: [x for x in my_posts if x['state'] == PostStates.CLOSED.value]}

    return my_sorted_posts


def get_closed_posts():
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.CLOSED.value},
    }
    return list(database.find(mango))
