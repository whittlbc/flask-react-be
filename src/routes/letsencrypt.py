import os
from flask_restplus import Resource
from flask import make_response
from src.routes import api

letsencrypt = api.namespace('.well-known')


@letsencrypt.route('/acme-challenge/<string:route_key>')
class LetsEncrypt(Resource):
  """
  Hit this endpoint when verifying your host for LetsEncrypt certificate creation
  Ensure LETSENCRYPT_ROUTE_KEY and LETSENCRYPT_RESPONSE_KEY are both set as
  environment variables first, though. These should be provided to you during the
  LetsEncrypt certificate request step
  """

  @letsencrypt.doc('letsencrypt_verification')
  def get(self, route_key):
    route_key_truth = os.environ.get('LETSENCRYPT_ROUTE_KEY')

    if not route_key_truth or route_key != route_key_truth:
      return '', 404

    resp_key = os.environ.get('LETSENCRYPT_RESPONSE_KEY')

    if not resp_key:
      return '', 500

    resp = make_response(resp_key)
    resp.headers['content-type'] = 'text/plain'

    return resp