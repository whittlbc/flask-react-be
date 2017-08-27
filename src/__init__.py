import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.helpers.definitions import configs_dir
from src.helpers.env import env, is_prod

app = Flask(__name__)
app.config.from_pyfile('{}/{}.py'.format(configs_dir, env()))

app.logger.addHandler(logging.FileHandler('main.log'))
app.logger.setLevel(logging.INFO)
logger = app.logger

db = SQLAlchemy(app)

from src.routes import api
api.init_app(app)

if is_prod() and os.environ.get('REQUIRE_SSL') == 'true':
  from flask_sslify import SSLify
  SSLify(app)