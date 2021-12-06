import couchdb
import dotenv


class DatabaseService:

    def __init__(self):
        envfile = dotenv.dotenv_values(".env")

        username = envfile.get("DBUsername")
        password = envfile.get("DBPassword")
        host = envfile.get("DBHost")

        server = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))
        self.database = server["pfe-df-g4"]

    def get_document(self, _document):
        print(self.database, _document)
        return self.database.get(_document)
