import dotenv
from flask import Flask

from errorHandler import error_handler
from routes import users, posts, addresses, categories

app = Flask(__name__)
envFile = dotenv.dotenv_values(".env")

# Routes
app.register_blueprint(users.get_blueprint(), url_prefix='/users')
app.register_blueprint(posts.get_blueprint(), url_prefix='/posts')
app.register_blueprint(addresses.get_blueprint(), url_prefix='/addresses')
app.register_blueprint(categories.get_blueprint(), url_prefix='/categories')

# HTTP errors handler
app.register_error_handler(400, error_handler.handle_400_error)
app.register_error_handler(401, error_handler.handle_401_error)
app.register_error_handler(404, error_handler.handle_404_error)
app.register_error_handler(500, error_handler.handle_500_error)
