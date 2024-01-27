import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    FLASK_APP = 'app'
