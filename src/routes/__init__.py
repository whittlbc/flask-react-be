from flask_restplus import Api

api = Api(version='0.1', title='MyAppName API')
namespace = api.namespace('api')

# Add all route handlers here:
from user import *