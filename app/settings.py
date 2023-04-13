import os

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ.get("SECRET_KEY")
SETTINGS = True
ENV_CONFIG = ".env"