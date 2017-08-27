from src import db
import datetime


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), index=True, unique=True)
  name = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=True)
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, email, name, password):
    self.email = email
    self.name = name
    self.password = password

  def __repr__(self):
    return '<User id={}, email={}, name{}, password={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.email, self.name, self.password, self.is_destroyed, self.created_at)