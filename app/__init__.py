import os
from flask import Flask
from flask_bcrypt import Bcrypt


SECRET_KEY = os.urandom(32)
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "*")
    app.config.from_object('app.config.Config')
    bcrypt.init_app(app)

    return app