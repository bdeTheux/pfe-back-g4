from couchdb.mapping import Document, TextField, BooleanField, ListField


class User(Document):  # if error, try import couchdb.document maybe
    _id = TextField()
    last_name = TextField()
    first_name = TextField()
    email = TextField()
    password = TextField()
    campus = TextField()
    favorites = ListField(TextField(), default=[])
    is_banned = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    def get_limited_data(self):
        return {"_id": self.id, "last_name": self.last_name, "first_name": self.first_name, "email": self.email,
                "campus": self.campus, "favorites": self.favorites}

    def get_data(self):
        data = self.get_limited_data()
        data["is_banned"] = self.is_banned
        data["is_admin"] = self.is_admin
        return data
