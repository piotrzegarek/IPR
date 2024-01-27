from flask import Flask, jsonify
from flask_wtf import CSRFProtect
# from app.models import db
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
# db.init_app(app)


@app.route("/")
def read_root():
    return jsonify(hello="world")