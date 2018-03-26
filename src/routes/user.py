from flask import request
from flask_restplus import Resource, fields
from src import dbi, logger
from src.api_responses.errors import *
from src.api_responses.success import *
from src.helpers.definitions import auth_header_name
from src.helpers.user_helper import current_user
from src.models import User
from src.routes import namespace, api
from src.utils import auth_util

# Models used to "match" what a request's params should look like
create_user_model = api.model('User', {
  'email': fields.String(required=True),
  'name': fields.String(required=True),
  'password': fields.String(required=True)
})

user_login_model = api.model('User', {
  'email': fields.String(required=True),
  'password': fields.String(required=True)
})


@namespace.route('/user')
class CreateUser(Resource):
  """Lets you POST to create a new user"""

  @namespace.doc('create_user')
  @namespace.expect(create_user_model, validate=True)
  def post(self):
    # Parse our payload.
    email = api.payload['email']
    name = api.payload['name']
    password = api.payload['password']

    # Ensure the email isn't taken already.
    if dbi.find_one(User, {'email': email}):
      return ACCOUNT_ALREADY_EXISTS

    try:
      # Create the new user
      user = dbi.create(User, {
        'email': email,
        'name': name,
        'hashed_pw': auth_util.hash_pw(password)
      })
    except BaseException as e:
      logger.error('Error creating new user, with error: {}'.format(e))
      return ERROR_CREATING_USER

    # Create a new session for the user
    session = user.new_session()
    token = auth_util.serialize_token(session.id, session.token)

    # Return success with newly created session token as response header
    return {'ok': True, 'message': 'Successfully Created User'}, 201, {auth_header_name: token}


@namespace.route('/user/login')
class UserAuth(Resource):
  """Login as a User"""

  @namespace.doc('user_login')
  @namespace.expect(user_login_model, validate=True)
  def post(self):
    # Parse our payload.
    email = api.payload['email']
    password = api.payload['password']

    # Find user by email
    user = dbi.find_one(User, {'email': email})

    # Ensure user exists
    if not user:
      return USER_NOT_FOUND

    # Ensure passwords match
    if not auth_util.verify_pw(user.hased_pw, password):
      return AUTHENTICATION_FAILED

    # Create a new session for the user
    session = user.new_session()
    token = auth_util.serialize_token(session.id, session.token)

    # Return success with newly created session token as response header
    return {'ok': True, 'message': 'User Login Succeeded'}, 200, {auth_header_name: token}


@namespace.route('/user/example_authed_get_request')
class ExampleAuthedGetRequest(Resource):
  """Example Authed Get Request"""

  def get(self):
    # How you would validate the request came from an authed user
    user = current_user()

    # Error out if unauthorized request
    if not user:
      return UNAUTHORIZED

    # Parse our payload from args
    payload = dict(request.args.items())

    # Get resource

    return {}, 200