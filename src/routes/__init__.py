from flask_restplus import Api

api = Api(version='0.1', title='MyAppName API')
namespace = api.namespace('api')

# After adding new route handler files, make sure to add them here in the same format:
# from <filename> import *
from user import *