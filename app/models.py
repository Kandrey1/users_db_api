import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    create = db.Column(db.DateTime, default=datetime.datetime.today())

    param = db.relationship('Parameter', backref='user', uselist=False, )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.name}>"


class Parameter(db.Model):
    __tablename__ = 'parameter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),)
    type_p = db.Column(db.String(150))
    value = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, type_p, value, user_id):
        self.name = name
        self.type_p = type_p
        self.value = value
        self.user_id = user_id

    def __repr__(self):
        return f"<{self.name} - {self.type_p} - {self.value}>"


class ParameterSchema(ma.Schema):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'type_p', 'value')
