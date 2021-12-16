import uuid

from werkzeug.security import generate_password_hash


def init_database(db):
    print("Database reinitialization asked")
    for doc in db:
        db.delete(db[doc])

    # Creating documents
    # USERS

    password = generate_password_hash("azerty")
    admin = uuid.uuid4().hex
    kevin = uuid.uuid4().hex
    narjis = uuid.uuid4().hex
    nina = uuid.uuid4().hex
    boris = uuid.uuid4().hex
    samy = uuid.uuid4().hex

    db[admin] = dict(type='User', last_name='admin',
                     first_name='admin', email='admin@vinci.be', favorites=[],
                     password=password, campus='Ixelles', is_banned=False, is_admin=True)
    db[kevin] = dict(type='User', last_name='Jullien',
                     first_name='Kevin', email='kevin.jullien@student.vinci.be', favorites=[],
                     password=password, campus='Woluwe', is_banned=False, is_admin=False)
    db[narjis] = dict(type='User', last_name='Laraki',
                      first_name='Narjis', email='narjis.laraki@student.vinci.be', favorites=[],
                      password=password, campus='Louvain-la-Neuve', is_banned=False,
                      is_admin=False)
    db[nina] = dict(type='User', last_name='Heuzer',
                    first_name='Nina', email='nina.heuzer@student.vinci.be', favorites=[],
                    password=password, campus='Ixelles', is_banned=False,
                    is_admin=False)
    db[boris] = dict(type='User', last_name='de Theux',
                     first_name='Boris', email='boris.detheux@student.vinci.be', favorites=[],
                     password=password, campus='Louvain-la-Neuve', is_banned=False,
                     is_admin=False)
    db[samy] = dict(type='User', last_name='Alliche',
                    first_name='Samy', email='samy.alliche@student.vinci.be', favorites=[],
                    password=password, campus='Louvain-la-Neuve', is_banned=False,
                    is_admin=False)

    # CATEGORIES
    db['Maison et Jardin'] = dict(type='Category', name='Maison et Jardin', parent=None,
                                  sub_categories=['Outils', 'Meubles', 'Pour la maison', 'Jardin',
                                                  'Electroménager'])
    db['Outils'] = dict(type='Category', name='Outils', parent='Maison et Jardin', sub_categories=[])
    db['Meubles'] = dict(type='Category', name='Meubles', parent='Maison et Jardin', sub_categories=[])
    db['Pour la maison'] = dict(type='Category', name='Pour la maison', parent='Maison et Jardin',
                                sub_categories=[])
    db['Jardin'] = dict(type='Category', name='Jardin', parent='Maison et Jardin', sub_categories=[])
    db['Electroménager'] = dict(type='Category', name='Electroménager', parent='Maison et Jardin',
                                sub_categories=[])

    db['Famille'] = dict(type='Category', name='Famille', parent=None,
                         sub_categories=['Santé et beauté', 'Fournitures pour animaux',
                                         'Puériculture et enfants',
                                         'Jouets et jeux'])
    db['Santé et beauté'] = dict(type='Category', name='Santé et beauté', parent='Famille', sub_categories=[])
    db['Fournitures pour animaux'] = dict(type='Category', name='Fournitures pour animaux', parent='Famille',
                                          sub_categories=[])
    db['Puériculture et enfants'] = dict(type='Category', name='Puériculture et enfants', parent='Famille',
                                         sub_categories=[])
    db['Jouets et jeux'] = dict(type='Category', name='Jouets et jeux', parent='Famille', sub_categories=[])

    db['Vêtements et accessoires'] = dict(type='Category', name='Vêtements et accessoires', parent=None,
                                          sub_categories=['Sacs et bagages', 'Vêtements et chaussures femmes',
                                                          'Vêtements et chaussures hommes',
                                                          'Bijoux et accessoires'])
    db['Sacs et bagages'] = dict(type='Category', name='Sacs et bagages',
                                 parent='Vêtements et accessoires', sub_categories=[])
    db['Vêtements et chaussures femmes'] = dict(type='Category', name='Vêtements et chaussures femmes',
                                                parent='Vêtements et accessoires', sub_categories=[])
    db['Vêtements et chaussures hommes'] = dict(type='Category', name='Vêtements et chaussures hommes',
                                                parent='Vêtements et accessoires', sub_categories=[])
    db['Bijoux et accessoires'] = dict(type='Category', name='Bijoux et accessoires',
                                       parent='Vêtements et accessoires', sub_categories=[])

    # POSTS
    giving = "À donner"
    selling = "À vendre"

    pending = 'En attente d\'approbation'
    approved = 'Approuvé'
    closed = 'Clôturé'

    generic_image = [
        "https://res.cloudinary.com/dbdblxnfi/image/upload/v1639385026/samples/ecommerce/accessories-bag.jpg"]
    # Pending
    db[uuid.uuid4().hex] = dict(type='Post', post_nature=giving, state=pending,
                                title='Lacet bleu',
                                description='Un seul lacet, 28cm',
                                places=['Woluwe', 'Ixelles'],
                                seller_id=kevin, price=0,
                                category_id='Vêtements et accessoires',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=pending,
                                title='Furet mâle',
                                description='En forme, 3 ans, aime manger les lacets bleus',
                                places=['Woluwe', 'Ixelles'],
                                seller_id=kevin, price=25,
                                category_id='Famille',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=pending,
                                title='Converses blanches',
                                description='En très bon état, pointure 38',
                                places=['Woluwe'],
                                seller_id=narjis, price=35.5,
                                category_id='Vêtements et chaussures femmes',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=pending,
                                title='Éperons portés par Billy the kid',
                                description="Tout est dans le titre, c'est pas un fake!",
                                places=['Woluwe', 'Louvain-la-Neuve'],
                                seller_id=nina, price=120000.3,
                                category_id='Fournitures pour animaux',
                                images=generic_image, video=None)

    # Accepted
    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=approved,
                                title='Petite robe noire',
                                description='Comme neuve',
                                places=['Ixelles'],
                                seller_id=narjis, price=20,
                                category_id='Vêtements et chaussures femmes',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=approved,
                                title='Recette de cocktail',
                                description='Une base gingembre, évidemment! De quoi rester en bonne santé',
                                places=['Woluwe'],
                                seller_id=boris, price=1.5,
                                category_id='Vêtements et chaussures femmes',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=giving, state=approved,
                                title='Talent',
                                description="Non, peut-être?",
                                places=['Louvain-la-Neuve'],
                                seller_id=samy, price=0,
                                category_id='Vêtements et chaussures femmes',
                                images=generic_image, video=None)

    # Closed
    db[uuid.uuid4().hex] = dict(type='Post', post_nature=giving, state=closed,
                                title='Vieux paquet de chips',
                                description='Il en reste 3, paprika, à peine humides',
                                places=['Ixelles'],
                                seller_id=kevin, price=0,
                                category_id='Santé et beauté',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=selling, state=closed,
                                title='Mazda rouge',
                                description='Superbe voiture',
                                places=['Ixelles'],
                                seller_id=nina, price=14999.9,
                                category_id='Electroménager',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=giving, state=closed,
                                title='Papier peint',
                                description='Rouge et vert',
                                places=['Ixelles'],
                                seller_id=boris, price=0,
                                category_id='Reserve',
                                images=generic_image, video=None)

    db[uuid.uuid4().hex] = dict(type='Post', post_nature=giving, state=closed,
                                title='Bonnet vert',
                                description='en laine',
                                places=['Louvain-la-Neuve'],
                                seller_id=nina, price=0,
                                category_id='Reserve',
                                images=generic_image, video=None)

    db['Woluwe'] = dict(type="Address", campus='Woluwe',
                        lat="50.849857061691836", long="4.453360810918974")
    db['Louvain-la-Neuve'] = dict(type="Address", campus='Louvain-la-Neuve',
                                  lat="50.670452676255934", long="4.611500148709881")
    db['Ixelles'] = dict(type="Address", campus='Ixelles',
                         lat="50.835525846476465", long="4.376626359487836")


def display_db_docs(database):
    print("Database documents asked")
    documents = []
    for doc in database:
        documents.append(database[doc])
    return documents
