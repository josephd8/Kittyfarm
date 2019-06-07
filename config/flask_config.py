ENV = "dev"

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "kittyfarm"
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/kitties.db'
HOME_ENGINE_STRING = 'sqlite:///data/kitties.db'
MODEL_CONFIG = "config/model_config.yml"
PATH_TO_MODEL = "models/kitties_model.pkl"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

if(ENV == "dev"):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/kitties.db'
    HOME_ENGINE_STRING = 'sqlite:///data/kitties.db'
# else:
#     # SQLALCHEMY_DATABASE_URI = rds uri here
#     # HOME_ENGINE_STRING = rds something here