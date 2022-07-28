from flask import request
from flask_restful import Resource
from sqlalchemy import update

from ..models import db, User, Parameter, ParameterSchema


def save_parameter(parameter):
    try:
        db.session.add(parameter)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True


class CustomError(Exception):
    pass


class AddParameter(Resource):
    """ POST запрос на установку параметра. Выполняет проверку на наличие
        User в БД, иначе выдает исключение. Если User существет добавляет
        новый параметр, либо перезаписывает существующий.
    """
    def post(self, user_name, param_name, param_type, param_value):
        """
        :param
            user_name: string - имя User
            param_name: string - имя параметра,
            param_type: string - тип параметра,
            param_value: string - значение параметра.
        """
        try:
            user = User.query.filter(User.name == user_name).first()
            if not user:
                raise CustomError(f'Невозможно установить параметры т.к. User '
                                  f'с именем <{user_name}> отсутствует в БД ')

            param = Parameter.query.filter(Parameter.user_id == user.id,
                                           Parameter.name == param_name).first()

            if param:
                db.session.execute(update(Parameter).
                                   where(Parameter.id == param.id).
                                   values(name=param_name,
                                          type_p=param_type,
                                          value=param_value))
            else:
                new_param = Parameter(name=param_name,
                                      type_p=param_type,
                                      value=param_value,
                                      user_id=user.id)
                db.session.add(new_param)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return {'message': f'<{e}>'}

        return {'message': 'Данные добавлены'}


class GetParameter(Resource):
    """ Get запрос возвращает json с данными по искомому (одному) параметру."""
    def get(self, user_name, path_url):
        """
        :param user_name: string - имя User,
               path_url: string - часть url содержит имя параметра и его тип
        """
        try:
            datas = list()
            param_schema = ParameterSchema(many=True)

            user = User.query.filter(User.name == user_name).first()
            if not user:
                return {'message': f'User с именем <{user_name}>'
                                   f' отсутствует в БД '}

            path_list = path_url.split('/')

            if len(path_list) != 2:
                return {'message': f'Указанный пусть некорректен'}
            else:
                params = Parameter.query.filter(Parameter.name == path_list[0],
                                        Parameter.type_p == path_list[1]).all()
            datas = param_schema.dump(params)

        except Exception as e:
            return {'message': f'Ошибка чтения из БД <{e}>'}

        return datas


class GetAllParameterUser(Resource):
    """ Get запрос возвращает json содержащий все параметры для User в запросе.
        user_name: string - имя User
    """
    def get(self, user_name):
        """
        :param user_name: string - имя User
        :return: json {'': [{},{}...]}
        """
        try:
            all_param = dict()
            param_schema = ParameterSchema(many=True)

            user = User.query.filter(User.name == user_name).first()
            if not user:
                raise CustomError(f'Error. User с именем <{user_name}> '
                                  f'отсутствует в БД ')

            parameters = Parameter.query.filter(
                                     Parameter.user_id == user.id).all()

            all_param[user.name] = param_schema.dump(parameters)

        except Exception as e:
            return {'message': f'Ошибка. <{e}>'}
        return all_param


class AddParametersWithJson(Resource):
    """ Post запрос на установку параметров(нескольких) для User в БД.
        Передается json с параметрами.{"Query":[{
                                            "Operation":"SetParam",
                                            "Name":"<имяпараметра>",
                                            "Type":"<тип параметра>",
                                            "Value":"<значение параметра>"}]}
    """
    def post(self, user_name):
        """
        :param user_name: string - имя User
        :return:  json {"Result": [{
                                       "Operation":"SetParam",
                                       "Name":"<имяпараметра>",
                                       "Type":"<типпараметра>",
                                       "Status":"OK|ERROR"
                                    }]}
        """
        results = {"Result": []}

        user = User.query.filter(User.name == user_name).first()
        if not user:
            return {'message': f' Невозможно установить параметры т.к. User'
                               f' с именем <{user_name}> отсутствует в БД '}

        datas = request.get_json()
        for data in datas['Query']:
            result = dict()
            try:
                result["Operation"] = data["Operation"]
                result["Name"] = data["Name"]
                result["Type"] = data["Type"]

                if data['Operation'] == 'SetParam':

                    new_param = Parameter(name=data['Name'],
                                          type_p=data['Type'],
                                          value=data['Value'],
                                          user_id=int(user.id))

                    res = save_parameter(new_param)
                    result["Status"] = 'OK' if res else 'ERROR'

                results['Result'].append(result)
            except Exception as e:
                pass

        return results
