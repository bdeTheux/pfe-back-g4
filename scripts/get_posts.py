from datetime import datetime

import couchdb
import dotenv
import pandas as pd

from models.Post import Post

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
server = couchdb.Server('http://%s:%s@%s:5984' % (username, password, host))

database = server["pfe-df-g4"]

mango = {
    'selector': {'type': 'Post', 'category_id': "Reserve"},
}

reserve = list(database.find(mango))

if not reserve:
    print("Aucune annonce en réserve")
if reserve:
    df = pd.DataFrame(reserve)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(df.head())
    time = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    name = f"{time}_reserve.csv"
    print(name)
    df.to_csv(name)

    response = input("Remove extracted posts from the DB? 'Y' for yes")
    if response == 'Y':
        for post in reserve:
            print(f"Deletion of {post}")
            elem = Post.load(post, database)
            database.delete(post)
