import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    FLASK_APP = 'app'
    FLASK_RUN_PORT=5001
    SECRET_KEY = os.getenv("SECRET_KEY", "*")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False