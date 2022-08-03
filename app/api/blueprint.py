from flask import Blueprint
from flask_restful import Api
from .controllers import AddParameter, GetParameterUser,\
    AddParametersWithJson, GetAllParameterUser


api_bp = Blueprint('/', __name__)
api = Api(api_bp)

# Route
api.add_resource(AddParameter, '/POST/api/parameters/'
                               '<string:user_name>/'
                               '<string:param_name>/'
                               '<string:param_type>/'
                               '<string:param_value>')

api.add_resource(GetParameterUser, '/GET/api/parameters/<string:user_name>')

api.add_resource(GetAllParameterUser, '/GET/api/parameters')

api.add_resource(AddParametersWithJson, '/POST/api/<string:user_name>')
