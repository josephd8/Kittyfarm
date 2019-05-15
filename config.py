import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "kittyfarm"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "app/kittyDB.db")
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"

