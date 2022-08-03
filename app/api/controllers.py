from flask import request
from flask_restful import Resource
from sqlalchemy import update

from ..models import db, User, Parameter, ParameterSchema


class AddParameter(Resource):
    """ POST запрос на установку параметра. Выполняет проверку на наличие
        User в БД, иначе выдает исключение. Если User существует, то добавляет
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
            user = UserDb().get_user(user_search=user_name)

            param = {'name': param_name, 'type_p': param_type,
                     'value': param_value}

            SetParameter().set(user_id=user.id, param=param)

        except Exception as e:
            return {'message': f'<{e}>'}

        return {'message': 'Данные добавлены'}


class GetParameterUser(Resource):
    """ Get запрос ( ?name=&type= ) возвращает json с данными в
        зависимости от наличия параметров:
        user задается в url
        name - имя параметра.
        type - тип параметра.
        Если нет name возвращает Error.
    """
    def get(self, user_name):
        try:
            datas = dict()
            param_schema = ParameterSchema(many=True)

            param_name = request.args.get('name')
            type_p = request.args.get('type')

            user = UserDb().get_user(user_name)

            if not param_name:
                raise Exception('Не задано имя параметра')

            if not type_p:
                params = Parameter.query.filter(
                    Parameter.name == param_name,
                    Parameter.user_id == user.id).all()
                datas[user.name] = param_schema.dump(params)
            else:
                datas[user.name] = param_schema.dump(user.param)

        except Exception as e:
            return {'message': f'Error. <{e}>'}

        return datas


class GetAllParameterUser(Resource):
    """ Get запрос ( ?user= ) возвращает json со всеми параметрами пользователя.
        Если user нет в БД возвращает Error.
    """
    def get(self):
        try:
            datas = dict()
            param_schema = ParameterSchema(many=True)

            user_name = request.args.get('user')

            user = UserDb().get_user(user_name)

            datas[user.name] = param_schema.dump(user.param)

        except Exception as e:
            return {'message': f'Error. <{e}>'}

        return datas


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
        try:
            results = {"Result": []}

            user = UserDb().get_user(user_name)

            datas = request.get_json()

            for data in datas['Query']:
                result = dict()

                result["Operation"] = data["Operation"]
                result["Name"] = data["Name"]
                result["Type"] = data["Type"]

                if data['Operation'] == 'SetParam':

                    new_param = {'name': data['Name'],
                                 'type_p': data['Type'],
                                 'value': data['Value']}

                    res = SetParameter().set(user_id=user.id,
                                             param=new_param)

                    result["Status"] = 'OK' if res else 'ERROR'

            results['Result'].append(result)

        except Exception as e:
            return {'message': f'Error. <{e}>'}

        return results


class UserDb:
    """ Позволяет создавать нового пользователя и получать всех
        пользователей из БД.
    """
    def _check(self, user_check: str):
        """ Проверяет есть ли такой пользователь в БД.
            :returns
                True - Если пользователь уже есть в БД.
                False - Если пользователя НЕТ в БД.
        """
        user_db = User.query.filter(User.name == user_check).first()

        if user_db:
            return True

        return False

    def add(self, new_user: str):
        """ Добавляет пользователя в БД """
        try:
            self.new_user = new_user

            if not self._check(self.new_user):
                user = User(name=self.new_user)
                db.session.add(user)
                db.session.commit()
            else:
                raise Exception(f'Пользователь с именем <{self.new_user}> '
                                f'уже существует')
        except Exception as e:
            raise Exception('Ошибка записи в БД')

    def get_user(self, user_search: str) -> object:
        """ Возвращает пользователя если есть в БД, иначе ошибку.
            :param user_search: string - имя пользователя
        """
        self.user_search = user_search

        if not self._check(self.user_search):
            raise Exception(f'Пользователь с именем <{user_search}> '
                            f'отсутствует в БД ')

        user = User.query.filter(User.name == self.user_search).first()

        return user


class SetParameter:
    """ Проверяет и записывает в БД параметр для существующего пользователя """
    def set(self, user_id: int, param: dict):
        """ Устанавливает параметр в БД, если параметр существует, то
            перезаписывает его.
            :param user_id: int - id пользователя
                   param: dict - параметры для записи в словаре
            :returns Error если запись не удалась
        """
        try:
            self.user_id = user_id
            self.name = param.get('name')
            self.type_p = param.get('type_p')
            self.value = param.get('value')

            if self._check():
                self._save()
        except Exception as e:
            raise

    def _check(self):
        """ Проверяет значение параметра на соответствие типа """
        valid_type = ['str', 'int']
        if self.type_p not in valid_type:
            raise Exception(f'Тип <{self.type_p}> '
                            f'недопустим для параметра')
        # str проверка:
        # isalnum() строка состоит только из букв и цифр
        # isalpha() строка состоит только из букв
        if not ((self.value.isdigit() and self.type_p == 'int') or (
             self.value.isalpha() and self.type_p == 'str')):
            raise Exception(f'Значение <{self.value}> не соответствует'
                            f' типу <{self.type_p}>')
        return True

    def _save(self):
        """ Устанавливает параметр в БД, если параметр существует, то
            перезаписывает его.
            :returns Error если запись не удалась
        """
        try:
            parameter = Parameter.query.filter(
                Parameter.user_id == self.user_id,
                Parameter.name == self.name).\
                first()

            if parameter and self.type_p == parameter.type_p:
                db.session.execute(update(Parameter).
                                   where(Parameter.id == parameter.id).
                                   values(value=self.value))
            else:
                new_param = Parameter(name=self.name,
                                      type_p=self.type_p,
                                      value=self.value,
                                      user_id=self.user_id)
                db.session.add(new_param)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception('Ошибка записи в БД')

        return True


