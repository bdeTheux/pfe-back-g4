import couchdb
import dotenv

envFile = dotenv.dotenv_values("../.env")

USERNAME = envFile.get("DBDevUsername")
PASSWORD = envFile.get("DBDevPassword")
HOST = envFile.get("DBDevHost")

# connecting with couchdb server
couch = couchdb.Server('http://%s:%s@%s:5984' % (USERNAME, PASSWORD, HOST))

# creating database
try:
    db = couch.create("pfe-df-g4")
except Exception as e:
    couch.delete("pfe-df-g4")
    db = couch.create("pfe-df-g4")
print("database \'pfe-df-g4\' created")

# creating document
docPosts = {'name': 'posts', 'content': {}}
docUsers = {'name': 'users', 'content': {}}
docCategories = {'name': 'categories', 'content': {}}
docAddresses = {'name': 'addresses', 'content': {}}
listDocs = [docPosts, docUsers, docCategories, docAddresses]
for doc in listDocs:
    db.save(doc)
    print("document \'" + doc['name'] + "\' created")
    # fetching from the database
    print("name is : " + doc['name'])
