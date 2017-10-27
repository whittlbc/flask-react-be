import inspect
import json
import os
from src.helpers.env import env


class Config:
  DEBUG = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  def as_dict(self):
    attrs = inspect.getmembers(self, lambda a: not(inspect.isroutine(a)))
    attrs = [a for a in attrs if not (a[0].startswith('__') and a[0].endswith('__'))]
    return dict(attrs)

  def as_json_string(self):
    return json.dumps(self.as_dict(), sort_keys=True, indent=2)


class ProdConfig(Config):
  DEBUG = False
  URL = 'https://yourprodurl.com'

  def __init__(self):
    self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
  URL = 'http://localhost:3000'

  def __init__(self):
    self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestConfig(Config):
  URL = 'http://localhost:3000'

  def __init__(self):
    self.SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL')


def get_config():
  config_class = globals().get('{}Config'.format(env().capitalize()))
  return config_class()