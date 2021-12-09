import uuid

import couchdb
import dotenv
from werkzeug.security import generate_password_hash

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
except Exception as e:
    print(e)
    couch.delete("pfe-df-g4")
    db = couch.create("pfe-df-g4")
print("database \'pfe-df-g4\' created")

# creating documents
## USERS
password = generate_password_hash("azerty")
db[uuid.uuid4().hex] = dict(type='User', last_name='admin',
                            first_name='admin', email='admin@vinci.be',
                            password=password, campus='Ixelles', is_banned=False, is_admin=True)
db[uuid.uuid4().hex] = dict(type='User', last_name='Jullien',
                            first_name='Kevin', email='kevin.jullien@student.vinci.be',
                            password=password, campus='Woluwe', is_banned=False, is_admin=False)
db[uuid.uuid4().hex] = dict(type='User', last_name='Laraki',
                            first_name='Narjis', email='narjis.laraki@student.vinci.be',
                            password=password, campus='Louvain-la-Neuve', is_banned=False,
                            is_admin=False)

## CATEGORIES
db['Maison et Jardin'] = dict(type='Category', name='Maison et Jardin', parent=None,
                              sub_categories=['Outils', 'Meubles', 'Pour la maison', 'Jardin', 'Electroménager'])
db['Outils'] = dict(type='Category', name='Outils', parent='Maison et Jardin', sub_categories=[])
db['Meubles'] = dict(type='Category', name='Meubles', parent='Maison et Jardin', sub_categories=[])
db['Pour la maison'] = dict(type='Category', name='Pour la maison', parent='Maison et Jardin', sub_categories=[])
db['Jardin'] = dict(type='Category', name='Jardin', parent='Maison et Jardin', sub_categories=[])
db['Electroménager'] = dict(type='Category', name='Electroménager', parent='Maison et Jardin', sub_categories=[])

db['Famille'] = dict(type='Category', name='Famille', parent=None,
                     sub_categories=['Santé et beauté', 'Fournitures pour animaux', 'Puériculture et enfants',
                                     'Jouets et jeux'])
db['Santé et beauté'] = dict(type='Category', name='Santé et beauté', parent='Famille', sub_categories=[])
db['Fournitures pour animaux'] = dict(type='Category', name='Fournitures pour animaux', parent='Famille',
                                      sub_categories=[])
db['Puériculture et enfants'] = dict(type='Category', name='Puériculture et enfants', parent='Famille',
                                     sub_categories=[])
db['Jouets et jeux'] = dict(type='Category', name='Jouets et jeux', parent='Famille', sub_categories=[])

db['Vêtements et accessoires'] = dict(type='Category', name='Vêtements et accessoires', parent=None,
                                      sub_categories=['Sacs et bagages', 'Vêtements et chaussures femmes',
                                                      'Vêtements et chaussures hommes', 'Bijoux et accessoires'])
db['Sacs et bagages'] = dict(type='Category', name='Sacs et bagages',
                             parent='Vêtements et accessoires', sub_categories=[])
db['Vêtements et chaussures femmes'] = dict(type='Category', name='Vêtements et chaussures femmes',
                                            parent='Vêtements et accessoires', sub_categories=[])
db['Vêtements et chaussures hommes'] = dict(type='Category', name='Vêtements et chaussures hommes',
                                            parent='Vêtements et accessoires', sub_categories=[])
db['Bijoux et accessoires'] = dict(type='Category', name='Bijoux et accessoires',
                                   parent='Vêtements et accessoires', sub_categories=[])

# docPosts = {'name': 'posts', 'content': {}}
# docAddresses = {'name': 'addresses', 'content': {}}
# listDocs = [docPosts, docUsers, docCategories, docAddresses]
# for doc in listDocs:
#     db.save(doc)
#     print("document \'" + doc['name'] + "\' created")
#     # fetching from the database
#     print("name is : " + doc['name'])
