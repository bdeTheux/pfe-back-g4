from couchdb.mapping import Document, TextField, BooleanField


class User(Document):  # if error, try import couchdb.document maybe
    _id = TextField()
    last_name = TextField()
    first_name = TextField()
    email = TextField()
    password = TextField()
    campus = TextField()  # for now, TODO -> find enum in couchdb.mapping doc
    is_banned = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    def to_public(self):
        return {"_id": self.id, "last_name": self.last_name, "first_name": self.first_name, "email": self.email,
                "campus": self.campus}

    def to_admin(self):
        return {"_id": self.id, "last_name": self.last_name, "first_name": self.first_name, "email": self.email,
                "campus": self.campus, "is_banned": self.is_banned, "is_admin": self.is_admin}
