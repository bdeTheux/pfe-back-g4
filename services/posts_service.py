import uuid

from db import database
from models.Post import Post, PostStates

database = database.get_database()


def _order_posts(posts, order=None):
    if order == 'asc':
        return sorted(posts, key=lambda i: (i['price']))
    if order == 'desc':
        return sorted(posts, key=lambda i: (i['price']), reverse=True)

    return posts


def get_posts(order=None):
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.APPROVED.value},
    }

    return _order_posts(list(database.find(mango)), order)


def get_posts_by_campus(campus, order=None):
    mango = {
        'selector': {'type': 'Post', 'state': PostStates.APPROVED.value},
    }
    list_posts = [row for row in list(database.find(mango)) if campus in row['places']]
    return _order_posts(list_posts, order)


def get_posts_by_category(category, order=None):
    print(category)
    mango = {
        'selector': {'type': 'Post',
                     'state': PostStates.APPROVED.value,
                     "category_id": category},
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
                             seller_id=post.seller_id, category_id=post.category_id, images=post.images)
    return id_post


def delete_post(_id):
    post = get_post_by_id(_id)
    return database.delete(post)


def edit_post(new_post, _id):
    previous_post = get_post_by_id(_id)
    new_post['state'] = previous_post['state']
    new_post['seller_id'] = previous_post['seller_id']
    for field in new_post:
        previous_post[field] = new_post[field]
    previous_post.store(database)
    return previous_post.get_data()


def get_posts_by_subcategory(category):
    mango = {
        'selector': {'type': 'Post',
                     'category_id': category,
                     'state': PostStates.APPROVED.value},
    }
    return list(database.find(mango))


def get_posts_by_campus_and_category(campus, category, order):
    posts_in_cat = get_posts_by_category(category)
    print(posts_in_cat)
    list_posts = [row for row in posts_in_cat if campus in row['places']]
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


def sell_one(_id):
    post = get_post_by_id(_id)
    post['state'] = PostStates.CLOSED.value
    post.store(database)
    return post.get_data()


def delete_image(_post, _image_name) -> bool:
    found = None
    for path in _post['images']:
        if _image_name in path:
            found = path
    if not found:
        AttributeError("L'image n'existe pas dans l'annonce donnée")
        print(found)
    _post['images'] = [x for x in _post['images'] if x != found]
    _post.store(database)
    return True
