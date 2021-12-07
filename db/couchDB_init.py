import couchdb
import dotenv

envFile = dotenv.dotenv_values("../.env")

USERNAME = envFile.get("DBUsername")
PASSWORD = envFile.get("DBPassword")
HOST = envFile.get("DBHost")

# connecting with couchdb server
couch = couchdb.Server('http://%s:%s@%s:5984' % (USERNAME, PASSWORD, HOST))

# creating database
try:
    db = couch.create("pfe-df-g4")
except:
    couch.delete("pfe-df-g4")
    db = couch.create("pfe-df-g4")
print("database \'pfe-df-g4\' created")

# creating document
docAnnounces = {'name': 'posts', 'content': {}}
docUsers = {'name': 'users', 'content': {}}
docCategories = {'name': 'categories', 'content': {}}
docAddresses = {'name': 'addresses', 'content': {}}
listDocs = [docAnnounces, docUsers, docCategories, docAddresses]
for doc in listDocs:
    db.save(doc)
    print("document \'" + doc['name'] + "\' created")
    # fetching from the database
    print("name is : " + doc['name'])
