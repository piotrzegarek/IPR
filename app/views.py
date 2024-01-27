from app import app
from flask import jsonify


@app.route("/")
def read_root():
    return jsonify(hello="dsadasd")