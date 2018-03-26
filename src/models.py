"""
Tables:

  User
  Session

Relationships:

  User --> has_many --> sessions
  Session --> belongs_to --> User
"""
import datetime
from src import db, dbi
from src.utils import auth_util
from uuid import uuid4


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String, index=True, unique=True, nullable=False)
  email = db.Column(db.String(120), index=True, unique=True)
  name = db.Column(db.String(120), nullable=False)
  hashed_pw = db.Column(db.String(240))
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, email=None, name=None, hashed_pw=None):
    self.email = email
    self.uid = uuid4().hex
    self.name = name
    self.hashed_pw = hashed_pw

  def new_session(self):
    return dbi.create(Session, {'user': self})

  def __repr__(self):
    return '<User id={}, uid={}, email={}, name{}, is_destroyed={}, created_at={}>'.format(
      self.id, self.uid, self.email, self.name, self.is_destroyed, self.created_at)


class Session(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
  user = db.relationship('User', backref='sessions')
  token = db.Column(db.String(64))

  def __init__(self, user=None, user_id=None, token=None):
    if user_id:
      self.user_id = user_id
    else:
      self.user = user

    self.token = token or auth_util.fresh_secret()

  def __repr__(self):
    return '<Session id={}, user_id={}>'.format(self.id, self.user_id)