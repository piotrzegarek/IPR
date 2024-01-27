from flask import Flask, jsonify
from flask_wtf import CSRFProtect
from app.models import db
from app.config import Config

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
csrf.init_app(app)
db.init_app(app)

from .views import *
