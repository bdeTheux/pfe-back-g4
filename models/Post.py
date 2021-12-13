from enum import Enum

from couchdb.mapping import Document, TextField, FloatField, ListField


class PostStates(Enum):
    PENDING = "En attente d'approbation"
    APPROVED = "Approuvé"
    REJECTED = "Refusé"
    CLOSED = "Clôturé"


class Post(Document):
    _id = TextField()
    post_nature = TextField()
    state = TextField()
    title = TextField()
    description = TextField()
    price = FloatField()
    places = ListField(TextField(), default=[])
    seller_id = TextField()
    category_id = TextField()
    images = ListField(TextField(), default=[])

    def get_data(self):
        return {"_id": self.id, "post_nature": self.post_nature, "state": self.state, "title": self.title,
                "description": self.description, "price": self.price, "places": self.places,
                "seller_id": self.seller_id, "category_id": self.category_id, "images": self.images}
