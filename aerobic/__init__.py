import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from env.config import oauth_credentials

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "env.config.DevelopmentConfig")
app.config.from_object(config_path)
app.config.from_object(oauth_credentials)

db = SQLAlchemy(app)

from . import api, views
from .database import Athlete, Activity

db.create_all()