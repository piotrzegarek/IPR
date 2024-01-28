from flask import Flask, jsonify
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from app.config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
csrf.init_app(app)


from app.models import *

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(id=username).first()

from .views import *
