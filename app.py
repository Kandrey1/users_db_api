from flask import Blueprint
from flask_restful import Api
from resources.request_api import RequestPostParameters, RequestPostJson, \
                                  RequestGetUser, RequestGetParameter


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(RequestPostParameters, '/POST/api/parameters/'
                                        '<string:user_name>/'
                                        '<string:param_name>/'
                                        '<string:param_type>/'
                                        '<string:param_value>')
api.add_resource(RequestGetParameter, '/GET/api/parameters/<string:user_name>/'
                                      '<string:param_name>/'
                                      '<string:param_type>')
api.add_resource(RequestGetUser, '/GET/api/parameters/<string:user_name>')

api.add_resource(RequestPostJson, '/POST/api/<string:user_name>')
