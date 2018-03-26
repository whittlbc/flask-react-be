from flask import request
from src import dbi
from src.helpers.definitions import auth_header_name
from src.helpers import decode_url_encoded_str
from src.models import Session
from src.utils.auth_util import unserialize_token


def current_user():
  auth_header = request.headers.get(auth_header_name)

  if not auth_header:
    return None

  token = decode_url_encoded_str(auth_header)
  session_info = unserialize_token(token)

  if not session_info.get('session_id') or not session_info.get('secret'):
    return None

  session = dbi.find_one(Session, {
    'id': session_info['session_id'],
    'token': session_info['secret']
  })

  if not session:
    return None

  return session.user