import couchdb

USERNAME = "admin"
PASSWORD = "SNKBN"
# connecting with couchdb server
couch = couchdb.Server('http://%s:%s@localhost:5984' % (USERNAME, PASSWORD))

# creating database
db = couch.create("pfe-df-g4")
print("database \'pfe-df-g4\' created")

# creating document
docAnnounces = {'name': 'announces'}
docUsers = {'name': 'users'}
docCategories = {'name': 'categories'}
docAddresses = {'name': 'addresses'}
listDocs = [docAnnounces, docUsers, docCategories, docAddresses]
for doc in listDocs:
    db.save(doc)
    print("document \'" + doc['name'] + "\' created")
    # fetching from the database
    print("name is : " + doc['name'])
