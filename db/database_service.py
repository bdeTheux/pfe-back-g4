class DatabaseService:

    def __init__(self, database):
        self.database = database

    def get_document(self, _document):
        return self.database.get(_document)
