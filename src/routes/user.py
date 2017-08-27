from flask_restplus import Resource, fields
from src.models import User
from src.routes import namespace, api
from src import dbi
from src.helpers.status_codes import *

# "model" used to "match" what a requests params will/should look like
create_user_model = api.model('User', {
  'email': fields.String(required=True),
  'name': fields.String(required=True),
  'password': fields.String(required=False)
})


@namespace.route('/users')
class CreateUser(Resource):
  """Lets you POST to create a new user"""

  @namespace.doc('create_user')
  @namespace.expect(create_user_model, validate=True)
  def post(self):
    # We can guarantee these params exist with certainty due to @namespace.expect decorator
    create_params = {
      'email': api.payload['email'],
      'name': api.payload['name'],
      'password': api.payload['password']
    }

    dbi.create(User, create_params)

    return '', 201