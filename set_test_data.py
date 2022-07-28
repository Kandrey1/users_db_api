import random

from app import create_app
from config import Config
from app.models import db, User, Parameter

app = create_app(Config)


def create_user():
    """ Создает пользователей в БД """
    user_name = ['admin', 'user1', 'user2', 'user3', 'user4', 'user5', 'user6',
                 'user7', 'user8', 'user9', 'user10']
    user_data = list()

    with app.app_context():
        for u in user_name:
            users = User(name=f'{u}')
            user_data.append(users)

        db.session.add_all(user_data)
        db.session.commit()


def create_parameter():
    """ Создает параметры у пользователей """
    parameters = list()
    with app.app_context():
        for i in range(30):
            new_param = Parameter(name=f'param{i}',
                                  type_p=f'type{i}',
                                  value=f'value{i}',
                                  user_id=random.randint(1, 11))
            parameters.append(new_param)

        db.session.add_all(parameters)
        db.session.commit()


def set_data():
    create_user()
    create_parameter()


if __name__ == '__main__':
    set_data()
