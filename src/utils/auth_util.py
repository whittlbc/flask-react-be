"""
Utilities for account security.
"""
import base64
import hmac
import os
from passlib.hash import bcrypt, hex_sha512


def hash_pw(password):
  # type: (str) -> bytes
  """
  :param password: The password to hash.
  :returns: The hashed password.
  """
  return bcrypt.using(rounds=10).hash(hex_sha512.hash(password))


def verify_pw(hashed_password, password):
  # type (bytes, str) -> bool
  """
  :param: hashed_password. The hashed password.
  :param: password The password.

  >>> verify_pw(hash_pw('hunter2'), 'hunter2')
  True
  >>> verify_pw(hash_pw('hunter2'), 'hunter1')
  False
  >>> verify_pw(b'garbage', 'hunter1')
  False
  """
  try:
    return bcrypt.verify(hex_sha512.hash(password), hashed_password)
  except ValueError:
    return False


def fresh_secret():
  # type () -> str
  """
  :returns: 32 bytes of cryptographically secure randomness, base64 encoded.
            Safe for inclusion in urls. In particular, guaranteed not to
            include an '%' characters.
  """
  return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')


def verify_secret(secret1, secret2):
  """
  :returns: True if secret1 == secret2. Uses a constant time string compare.
  """
  return hmac.compare_digest(secret1, secret2)


def serialize_token(session_id, secret):
  """
  :returns: <session_id>%<secret>
  """
  return str(session_id) + '%' + secret


def unserialize_token(token):
  """
  :returns: {session_id, token}
  """
  session_id, secret = token.split('%')
  return dict(session_id=int(session_id), secret=secret)