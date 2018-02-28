import os
import sys
from flask import Flask
from logging import INFO, StreamHandler

# Create and configure the Flask app
app = Flask(__name__)

# Set up logging
app.logger.addHandler(StreamHandler(sys.stdout))
app.logger.setLevel(INFO)
logger = app.logger

# Set up API routes
from src.routes import api
api.init_app(app)

if os.environ.get('REQUIRE_SSL') == 'true':
  from flask_sslify import SSLify
  SSLify(app)