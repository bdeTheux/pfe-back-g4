from couchdb.mapping import Document, TextField, FloatField, ListField


class Post(Document):
    id = TextField(name="_id")
    post_nature = TextField()
    state = TextField()
    title = TextField()
    description = TextField()
    price = FloatField()
    address_id = ListField(TextField(), default=[])
    seller_id = TextField()
    category_id = TextField()

    def get_data(self):
        return {"id": self.id, "post_nature": self.post_nature, "state": self.state, "title": self.title,
                "description": self.description, "price": self.price, "address_id": self.address_id,
                "seller_id": self.seller_id, "category_id": self.category_id}
