from couchdb.mapping import Document, TextField


class Category(Document):
    _id = TextField()
    campus = TextField()
    lat = TextField()
    long = TextField()

    def get_data(self):
        return {"campus": self.campus, "lat": self.lat, "long": self.long}
