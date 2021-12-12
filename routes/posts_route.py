from flask import jsonify, abort, request, Blueprint

import services.posts_service as service
from models.Post import Post, PostStates
from utils.utils import admin_token_required, token_required, token_welcome

posts_route = Blueprint('posts-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return posts_route


@posts_route.route('/', methods=['GET'])
def get_all():
    category = request.args.get('category')
    campus = request.args.get('campus')
    if campus and category:
        return jsonify(service.get_posts_by_campus_and_category(campus, category))
    elif campus:
        return jsonify(service.get_posts_by_campus(campus))
    elif category:
        return jsonify(service.get_posts_by_category(category))

    return jsonify(service.get_posts())


@posts_route.route('/closed', methods=['GET'])
@admin_token_required
def get_closed(_current_user):
    return jsonify(service.get_closed_posts())


@posts_route.route('/pending', methods=['GET'])
@admin_token_required
def get_pending(_current_user):
    return jsonify(service.get_pending_posts())


@posts_route.route('/myPosts', methods=['GET'])
@token_required
def get_all_my_posts(_current_user):
    return jsonify(service.get_all_my_posts(_current_user['_id']))


@posts_route.route('/<string:_id>', methods=['GET'])
@token_welcome
def get_with_id(_current_user, _id):
    post = service.get_post_by_id(_id)
    if post:
        if post.state != PostStates.APPROVED:
            if not _current_user:
                return abort(401, "You can't do that")
            elif _current_user['is_admin'] or (post['seller_id'] == _current_user['id']):
                return jsonify(post.get_data())
        else:
            return jsonify(post.get_data())

    return abort(404, "This post doesn't exist")


@posts_route.route('/', methods=['POST'])
@token_required
def add_one(_current_user):
    if not request.json:
        abort(400, "The payload is empty")

    data = request.json
    post_nature = data['post_nature']
    title = data['title']
    description = data['description']
    price = 0
    if post_nature == 'À vendre':
        price = data['price']
    places = data.get('places', [])
    seller_id = _current_user['_id']
    category_id = data['category_id']
    post = Post(post_nature=post_nature,
                title=title,
                description=description,
                price=price,
                places=places,
                seller_id=seller_id,
                category_id=category_id,
                )

    res = service.create_post(post)
    return jsonify(res) if res else abort(400, "Something wrong happened")


@posts_route.route('/<string:_id>', methods=['DELETE'])
@token_required
def delete_one(_current_user, _id):
    try:
        res = service.delete_post(_id)
    except FileNotFoundError:
        abort(404, "Post not found")
    return jsonify(res)


@posts_route.route('/<string:_id>', methods=['PUT'])
@token_required
def edit_one(_current_user, _id):
    if not request.json:
        abort(400, "The payload is empty")

    data = request.json
    post = service.get_post_by_id(_id)
    if post['seller_id'] != _current_user['_id']:
        abort(401, "You can only change your own post")

    post_nature = data['post_nature']
    title = data['title']
    description = data['description']
    price = 0
    if post_nature != 'Giving':
        price = data['price']
    places = data['places']
    post = Post(post_nature=post_nature,
                title=title,
                description=description,
                price=price,
                places=places,
                )

    return jsonify(service.edit_post(post, _id))


@posts_route.route('/<string:_id>/stateChange', methods=['POST'])
@admin_token_required
def change_state(_current_user, _id):
    if not request.json:
        abort(400, "The payload is empty")
    data = request.json

    state = data['state']
    if state != PostStates.CLOSED.value and state != PostStates.PENDING.value and state != PostStates.APPROVED.value:
        abort(400,
              f"Valid states are {PostStates.PENDING.value}, {PostStates.APPROVED.value}, and {PostStates.CLOSED.value}")
    return jsonify(service.change_state(_id, state))
