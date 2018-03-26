"""API Error Responses"""

# Generic Errors
UNAUTHORIZED = {'ok': False, 'code': 401, 'error': 'unauthorized'}, 401
UNKNOWN_ERROR = {'ok': False, 'code': 500, 'error': 'unknown_error'}, 500
FORBIDDEN = {'ok': False, 'code': 403, 'error': 'forbidden'}, 403
INVALID_INPUT_PAYLOAD = {'ok': False, 'code': 400, 'error': 'invalid_input_payload'}, 400

# User Errors
USER_NOT_FOUND = {'ok': False, 'code': 1100, 'error': 'user_not_found'}, 404
ACCOUNT_ALREADY_EXISTS = {'ok': False, 'code': 1101, 'error': 'account_already_exists'}, 500
ERROR_CREATING_USER = {'ok': False, 'code': 1102, 'error': 'user_creation_error'}, 500
AUTHENTICATION_FAILED = {'ok': False, 'code': 1103, 'error': 'authentication_failed'}, 401