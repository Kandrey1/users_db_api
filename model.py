from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    pr = db.relationship('Parameters', backref='users', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<users {self.id}>"


class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    value = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, type, value, user_id):
        self.name = name
        self.type = type
        self.value = value
        self.user_id = user_id

    def __repr__(self):
        return f"<parameters {self.id}>"
