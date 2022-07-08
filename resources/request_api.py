from flask import request
from flask_restful import Resource
from model import db, Users, Parameters    # циклический импорт поэтому из model


class DataBase:
    def save(self, database, row):
        try:
            database.session.add(row)
            database.session.commit()
        except:
            db.session.rollback()
            return {'message': 'Ошибка записи в БД'}
        return False


def get_params(parameters):
    datas = []
    for parameter in parameters:
        data = {'name': parameter.name,
                'type': parameter.type,
                'value': parameter.value}
        datas.append(data)
    return datas


class RequestPostParameters(Resource):
    def post(self, user_name, param_name, param_type, param_value):
        try:
            user = Users.query.filter(Users.name == user_name).first()
            if not user:
                return {'message': f' Невозможно установить параметры т.к. User'
                                   f' с именем <{user_name}> отсутствует в БД '}

            parameters = Parameters.query.filter(
                                            Parameters.user_id == user.id).all()
            params = []
            for parameter in parameters:
                params.append(parameter.name)

            if param_name not in params:
                new_parameter = Parameters(name=param_name,
                                           type=param_type,
                                           value=param_value,
                                           user_id=user.id)

                DataBase().save(database=db, row=new_parameter)
            else:
                return {'message': 'Запись с таким параметром уже существуют'}
        except:
            return {'message': 'Ошибка записи в БД'}

        return {'message': 'Данные добавлены'}


class RequestGetParameter(Resource):
    def get(self, user_name, param_name, param_type):
        try:
            datas = []
            user = Users.query.filter(Users.name == user_name).first()
            if not user:
                return {'message': f'User с именем <{user_name}>'
                                   f' отсутствует в БД '}

            params = Parameters.query.filter((Parameters.name == param_name) &
                                        (Parameters.type == param_type)).all()

            datas = get_params(params)

        except:
            return {'message': 'Ошибка чтения из БД'}

        return datas


class RequestGetUser(Resource):
    def get(self, user_name):
        try:
            user = Users.query.filter(Users.name == user_name).first()
            parameters_user = {}

            if not user:
                return {'message': f'User с именем <{user_name}>'
                                   f' отсутствует в БД '}

            parameters = Parameters.query.filter(
                                     Parameters.user_id == user.id).all()

            datas = get_params(parameters)
            parameters_user[user.name] = datas

        except:
            return {'message': 'Ошибка чтения из БД'}

        return parameters_user


class RequestPostJson(Resource):
    def post(self, user_name):
        data = request.get_json()
        results = []
        for item in data.keys():
            parameter_set = data[item][0]
            user = Users.query.filter(Users.name == user_name).first()

            if not user:
                return {'message': f' Невозможно установить параметры т.к. User'
                                   f' с именем <{user_name}> отсутствует в БД '}

            new_param = Parameters(name=parameter_set['Name'],
                                   type=parameter_set['Type'],
                                   value=parameter_set['Value'],
                                   user_id=int(user.id))

            result = {"Result": [{"Operation": "SetParam",
                                  "Name": new_param.name,
                                  "Type": new_param.type,
                                  "Status": ""}]}

            res = DataBase().save(database=db, row=new_param)

            result["Result"][0]["Status"] = 'OK' if not res else 'ERROR'
            results.append(result)

        return results
