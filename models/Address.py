from couchdb.mapping import Document, TextField


class Address(Document):
    _id = TextField()
    campus = TextField()
    lat = TextField()
    long = TextField()

    def get_data(self):
        return {"_id": self._id, "campus": self.campus, "lat": self.lat, "long": self.long}
