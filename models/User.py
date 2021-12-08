from couchdb.mapping import IntegerField, Document, TextField, BooleanField


class User(Document):  # if error, try import couchdb.document maybe
    doc_type = 'users'

    id = IntegerField()
    public_id = TextField()  # -> must be len = 50 and unique, not sure parameters exist in couchdb -> also, see if it's automatically generated
    last_name = TextField()
    first_name = TextField()
    email = TextField()
    password = TextField()
    campus = TextField()  # for now, TODO -> find enum in couchdb.mapping doc
    is_banned = BooleanField(default=False)
