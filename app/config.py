import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    FLASK_APP = 'app'
    FLASK_DEBUG=True
    FLASK_RUN_PORT=5000
    SECRET_KEY = os.getenv("SECRET_KEY", "*")
    SQLALCHEMY_DATABASE_URI = 'postgresql://piotrzegarek:postgres@localhost:5432/ipr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False