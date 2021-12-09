import os

import couchdb
import dotenv

envfile = dotenv.dotenv_values(".env")
try:
    environment = os.environ["FLASK_ENV"]
except Exception:
    environment = "prod"
if environment == "development":
    username = envfile.get("DBDevUsername")
    password = envfile.get("DBDevPassword")
    host = envfile.get("DBDevHost")
else:
    username = os.environ["DBProdUsername"]
    password = os.environ["DBProdPassword"]
    host = os.environ["DBProdHost"]

server = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))

database = server["pfe-df-g4"]


def get_database():
    return database
