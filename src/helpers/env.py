import os

environment = os.environ.get('ENV')
assert environment

ENV = environment.lower()


def env():
  return ENV


def is_test():
  return ENV == 'test'


def is_dev():
  return ENV == 'dev'


def is_staging():
  return ENV == 'staging'


def is_prod():
  return ENV == 'prod'