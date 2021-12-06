import couchdb
import dotenv


class Database:

    def __init__(self):
        envfile = dotenv.dotenv_values(".env")

        username = envfile.get("DBUsername")
        password = envfile.get("DBPassword")
        host = envfile.get("DBHost")

        self.DATABASE = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))


class DatabaseService:

    def __init__(self, database):
        self.database = database
        print(database)

    def get_document(self, _document):
        print(self.database, _document)
        return self.database.get(_document)
