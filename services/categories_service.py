from db import database
from models.Category import Category

database = database.get_database()


def get_categories():
    mango = {
        'selector': {'type': 'Category'},
        'fields': ['name', 'parent', 'sub_categories']
    }
    return list(database.find(mango))


def get_categories_as_tree():
    mango = {
        'selector': {'type': 'Category', 'parent': None},
        'fields': ['name', 'parent', 'sub_categories']
    }
    dic = {x['name']: [] for x in database.find(mango)}
    dic = _get_sub({x['name']: [] for x in database.find(mango)})
    return dic


def _get_sub(dic):
    for cat in dic.keys():
        mango = {
            'selector': {'type': 'Category', 'parent': cat},
            'fields': ['name', 'sub_categories']
        }
        subs = _get_sub({x['name']: [] for x in database.find(mango)})
        if subs:
            dic[cat].append(subs)

    return dic


def get_category_by_id(_id):
    category = Category.load(database, _id)
    if not category:
        raise AttributeError("Reference not found")
    return category


def create_category(_name, _parent, _sub_categories):
    """Create a new category only if the same name does not exist already.
    Only existing parent and non-existing children are valid.
    Parameters
        [mandatory]
        - '_name': a non-empty string
        [optional]
        - '_parent' : the parent's id. Has to exist already in the DB
           and != than _name, or it will be set to None.
        - '_sub_categories' : a list of strings. If the categories in the list does not exist,
           they are created as sub_categories of the new one. If they exist, they are ignored.
    Returns
        The name (and id) of the added category
    """
    parent_category = None
    # Check the validity of the parent
    if _parent and _parent != _name:
        parent_category = Category.load(database, _parent)
    parent = parent_category.name if parent_category else None

    sub_categories = []

    if _sub_categories:
        for cat in _sub_categories:
            existing_cat = Category.load(database, cat)
            if not existing_cat:
                database[cat] = dict(type='Category', name=cat, parent=_name, sub_categories=[])
                sub_categories.append(cat)

    database[_name] = dict(type='Category', name=_name, parent=parent, sub_categories=sub_categories)

    if parent_category:
        parent_category.sub_categories.append(_name)
        parent_category.store(database)

    return _name


def delete_category(_id):
    """Delete a category and its sub-categories."""
    category = Category.load(database, _id)

    if not category:
        raise AttributeError("Reference not found")

    if category.parent:
        parent = Category.load(database, category.parent)
        parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
        parent.store(database)
    return _delete_category_and_sub_categories(category)


def _delete_category_and_sub_categories(node: Category) -> bool:
    if not node:
        return False
    for child in node.sub_categories:
        cat = Category.load(database, child)
        _delete_category_and_sub_categories(cat)
    database.delete(node)
    return True


def get_sub_categories(category: Category) -> bool:
    children = {category.name: category.get_data()}
    temp = [x for x in category.sub_categories]  # copy
    while temp:
        actual = temp.pop()
        cat = Category.load(database, temp.pop())
        children[cat.parent] = 0
        children.append(temp)
        get_sub_categories(cat, children)
    return True


def get_parents(_id) -> list:
    parents = []
    node = Category.load(database, _id)
    if not node:
        raise AttributeError("Reference not found")
    while True:
        if not node.parent:
            break
        parents.append(node.parent)
        node = Category.load(database, node.parent)

    return parents


def edit_category(_id, _name, _parent, _sub_categories):
    """Edit a category by its given id and the given data.
    Parameters
        [mandatory]
        - _name: does not have to be empty nor existing in the DB.
        - _parent has to either exist in the DB or to be null.
          if it is not null and does not exist, it is aborted
        - _sub_categories: has to be a list of strings.
          If it does not have the same items as the original in the DB, the operation is aborted.
          If it has additional items with parents, it is aborted.
          If it has additional unknown items, they are created.
    Returns
        The name (and id) of the added category
    """
    category = Category.load(database, _id)

    # If a new name is set
    if _name != category.name:
        if not _name:
            raise AttributeError("Name is empty")
        new_name = Category.load(database, _name)
        if new_name:
            raise AttributeError("Reference with same name found")

    # If sub_categories are missing, aborting
    missing_subs = set(category.sub_categories).difference(_sub_categories)
    if len(missing_subs) != 0:
        raise AttributeError("Cannot remove sub_categories when editing, please edit those sub_categories")

    # If new sub_categories already have a parent, aborting
    new_subs = set(_sub_categories).difference(category.sub_categories)
    for cat in new_subs:
        if not cat:
            raise AttributeError("Some newly added sub_categories have an empty name")
        c = Category.load(database, cat)
        if c and c.parent:
            raise AttributeError("Some newly added sub_categories have a parent category already")

    # If the parent is different
    if category.parent != _parent:
        if _parent:
            parent = Category.load(database, category.parent)
            if not parent:
                raise AttributeError("The parent category does not exist")
            parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
            parent.store(database)

        category.parent = _parent

    # For every new added sub_cat, create it or edit its parent
    for cat in new_subs:
        c = Category.load(database, cat)
        if c:
            c.parent = category.name
            c.store(database)
        else:
            create_category({"name": c, "parent": category.name})

    # If a new name is given, copy the actual category and rename the copy
    if _name != category.name:
        database.copy(category.name, _name)
        copy = Category.load(database, _name)
        copy.name = _name
        copy.store(database)

        # Change the parent of the sub_categories with the new name
        for sub in copy.sub_categories:
            c = Category.load(database, sub)
            c.parent = copy.name
            c.store(database)

        # Replacing the sub_category name in the parent's sub_categories list
        if copy.parent:
            parent = Category.load(database, copy.parent)
            parent.sub_categories = [cat for cat in parent.sub_categories if cat != category.name]
            parent.sub_categories.append(copy.name)

        # Former category deletion
        database.delete(category)
    return _name
