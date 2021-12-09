import dotenv
from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from errorHandler import error_handler
from routes import users, posts, addresses, categories, authentication

app = Flask(__name__)
CORS(app)
envFile = dotenv.dotenv_values(".env")

# Routes
app.register_blueprint(users.get_blueprint(), url_prefix='/users')
app.register_blueprint(posts.get_blueprint(), url_prefix='/posts')
app.register_blueprint(addresses.get_blueprint(), url_prefix='/addresses')
app.register_blueprint(categories.get_blueprint(), url_prefix='/categories')
app.register_blueprint(authentication.get_blueprint())

# HTTP errors handler
app.register_error_handler(HTTPException, error_handler.generic_http_handler)
