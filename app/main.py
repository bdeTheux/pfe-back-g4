import dotenv
from flask import Flask

from errorHandler import error_handler
from routes import request_api

app = Flask(__name__)
envFile = dotenv.dotenv_values(".env")

app.register_blueprint(request_api.get_blueprint())

app.register_error_handler(400, error_handler.handle_400_error)
app.register_error_handler(401, error_handler.handle_401_error)
app.register_error_handler(404, error_handler.handle_404_error)
app.register_error_handler(500, error_handler.handle_500_error)
