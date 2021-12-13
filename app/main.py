import os

import cloudinary
import dotenv
from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from errorHandler import error_handler
from routes import users_route, posts_route, addresses_route, categories_route, authentication_route, database_route

app = Flask(__name__)
CORS(app)

envfile = dotenv.dotenv_values(".env")
try:
    environment = os.environ["FLASK_ENV"]
except Exception:
    environment = "prod"
if environment == "development":
    cloud_name = envfile.get("cloudinary_cloud_name")
    api_key = envfile.get("cloudinary_api_key")
    api_secret = envfile.get("cloudinary_api_secret")
else:
    cloud_name = os.environ["cloudinary_cloud_name"]
    api_key = os.environ["cloudinary_api_key"]
    api_secret = os.environ["cloudinary_api_secret"]

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)

# Routes
app.register_blueprint(users_route.get_blueprint(), url_prefix='/users')
app.register_blueprint(posts_route.get_blueprint(), url_prefix='/posts')
app.register_blueprint(addresses_route.get_blueprint(), url_prefix='/addresses')
app.register_blueprint(categories_route.get_blueprint(), url_prefix='/categories')
app.register_blueprint(authentication_route.get_blueprint())

# Dev purpose
app.register_blueprint(database_route.get_blueprint(), url_prefix='/database')

# HTTP errors handler
app.register_error_handler(HTTPException, error_handler.generic_http_handler)
