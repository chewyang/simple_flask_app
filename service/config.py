import os
import tempfile
from datetime import timedelta

class Config(object):
    # TEMPLATE_FOLDER = '../templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "hello"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'test2.db')
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=1)