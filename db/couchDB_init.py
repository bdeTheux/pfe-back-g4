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
    db = couch["pfe-df-g4"]
    for doc in db:
        print("Deleting:", doc)
        db.delete(db[doc])
    couch.delete("pfe-df-g4")
    print("database \'pfe-df-g4\' deleted")
    db = couch.create("pfe-df-g4")
print("database \'pfe-df-g4\' created")

# Creating documents
# USERS
password = generate_password_hash("azerty")
id1 = uuid.uuid4().hex
id2 = uuid.uuid4().hex
id3 = uuid.uuid4().hex
db[id1] = dict(type='User', last_name='admin',
               first_name='admin', email='admin@vinci.be',
               password=password, campus='Ixelles', is_banned=False, is_admin=True)
db[id2] = dict(type='User', last_name='Jullien',
               first_name='Kevin', email='kevin.jullien@student.vinci.be',
               password=password, campus='Woluwe', is_banned=False, is_admin=False)
db[id3] = dict(type='User', last_name='Laraki',
               first_name='Narjis', email='narjis.laraki@student.vinci.be',
               password=password, campus='Louvain-la-Neuve', is_banned=False,
               is_admin=False)

# CATEGORIES
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

# POSTS
db[uuid.uuid4().hex] = dict(type='Post', post_nature='En vente', state='En attente d\'approbation',
                            title='Converses blanches',
                            description='En très bon état, pointure 38', address_id=['Woluwe'],
                            seller_id=id3, price=35.5,
                            category_id='Vêtements et chaussures femmes')
db[uuid.uuid4().hex] = dict(type='Post', post_nature='En vente', state='Approuvé', title='Petite robe noire',
                            description='Comme neuve', address_id=['Ixelles'],
                            seller_id=id3, price=20,
                            category_id='Vêtements et chaussures femmes')
db[uuid.uuid4().hex] = dict(type='Post', post_nature='À donner', state='Clôturé', title='Vieux paquet de chips',
                            description='Il en reste 3, paprika', address_id=['Ixelles'],
                            seller_id=id3, price=0,
                            category_id='Santé et beauté')
