from couchdb.mapping import Document, TextField, ListField


class Category(Document):
    id = TextField(name="_id")
    name = TextField()
    parent = TextField()
    sub_categories = ListField(TextField())

    def get_data(self):
        return {"name": self.name, "parent": self.parent, "sub_categories": self.sub_categories}
