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
    categories = request.args.get('category')
    campus = request.args.get('campus')
    order = request.args.get('order', None)
    print(order)
    if campus and categories:
        return jsonify(service.get_posts_by_campus_and_category(campus, categories, order))
    elif campus:
        return jsonify(service.get_posts_by_campus(campus, order))
    elif categories:
        return jsonify(service.get_posts_by_category(categories, order))

    return jsonify(service.get_posts(order))


@posts_route.route('/closed', methods=['GET'])
@admin_token_required
def get_closed(_current_user):
    return jsonify(service.get_closed_posts())


@posts_route.route('/pending', methods=['GET'])
@admin_token_required
def get_pending(_current_user):
    return jsonify(service.get_pending_posts())


@posts_route.route('/rejected', methods=['GET'])
@admin_token_required
def get_rejected(_current_user):
    return jsonify(service.get_rejected_posts())


@posts_route.route('/myPosts', methods=['GET'])
@token_required
def get_all_my_posts(_current_user):
    return jsonify(service.get_all_my_posts(_current_user['_id']))


@posts_route.route('/<string:_id>', methods=['GET'])
@token_welcome
def get_with_id(_current_user, _id):
    post = service.get_post_by_id(_id)
    if post:
        if post.state != PostStates.APPROVED.value:
            if _current_user['is_admin'] or (post['seller_id'] == _current_user['id']):
                return jsonify(post.get_data())
        else:
            return jsonify(post.get_data())

    return abort(404, "Cette annonce n'existe pas/plus.")


@posts_route.route('/', methods=['POST'])
@token_required
def add_one(_current_user):
    if not request.json:
        abort(400, "La requête est vide")

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
    return jsonify(res) if res else abort(500, "Il y a eu un problème.")


@posts_route.route('/<string:_id>', methods=['DELETE'])
@token_required
def delete_one(_current_user, _id):
    try:
        res = service.delete_post(_id)
    except FileNotFoundError:
        abort(404, "Cette annonce n'existe pas/plus.")
    return jsonify(res)


@posts_route.route('/<string:_id>', methods=['PUT'])
@token_required
def edit_one(_current_user, _id):
    if not request.json:
        abort(400, "La requête est vide")

    data = request.json
    post = service.get_post_by_id(_id)
    if post['seller_id'] != _current_user['_id']:
        abort(401,
              "Vous ne pouvez pas modifier cette annonce.")  # User can only change his own post, can admin ? -> TODO

    post_nature = data['post_nature']
    title = data['title']
    description = data['description']
    price = 0
    if post_nature != 'À donner':
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
        abort(400, "La requête est vide")
    data = request.json

    state = data['state']
    if state != PostStates.CLOSED.value and state != PostStates.PENDING.value and \
            state != PostStates.APPROVED.value and state != PostStates.REJECTED.value:
        abort(400,
              f"Les états valides sont {PostStates.PENDING.value}, {PostStates.APPROVED.value}"
              f", {PostStates.REJECTED.value}, et {PostStates.CLOSED.value}")
    return jsonify(service.change_state(_id, state))
