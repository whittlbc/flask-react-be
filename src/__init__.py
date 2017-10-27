from logging import StreamHandler, FileHandler, INFO
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import get_config
from src.helpers.env import is_prod

# Create and configure the Flask app
app = Flask(__name__)
app.config.from_object(get_config())

# Set up logging
if is_prod():
  app.logger.addHandler(StreamHandler(sys.stdout))
else:
  app.logger.addHandler(FileHandler('main.log'))

app.logger.setLevel(INFO)
logger = app.logger

# Set up Postgres DB
db = SQLAlchemy(app)

# Set up API routes
from src.routes import api
api.init_app(app)

if is_prod() and os.environ.get('REQUIRE_SSL') == 'true':
  from flask_sslify import SSLify
  SSLify(app)