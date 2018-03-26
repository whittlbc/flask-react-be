import os
from src.helpers.env import env


class Config:
  DEBUG = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
  DEBUG = False
  URL = 'https://yourprodurl.com'

  def __init__(self):
    self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class StagingConfig(Config):
  DEBUG = False
  URL = 'https://yourstagingurl.com'

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


config = get_config()