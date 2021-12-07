import couchdb
import dotenv

envfile = dotenv.dotenv_values("../.env")

response = input("""Type \"dev\" to edit the development DB
Type \"prod\" to edit the development DB
Type anything else to stop the script
""")

if response == "dev":
    username = envfile.get("DBDevUsername")
    password = envfile.get("DBDevPassword")
    host = envfile.get("DBDevHost")
elif response == "prod":
    username = envfile.get("DBProdUsername")
    password = envfile.get("DBProdPassword")
    host = envfile.get("DBProdHost")
else:
    exit(0)

# connecting with couchdb server
couch = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))

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
