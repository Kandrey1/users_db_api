from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from app import api_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(api_bp, url_prefix='/')

db = SQLAlchemy(app)

# ошибка циклического импорта поэтому тут модели
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
    type = db.Column(db.String(50),  unique=True)
    value = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, type, value, user_id):
        self.name = name
        self.type = type
        self.value = value
        self.user_id = user_id


if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')
