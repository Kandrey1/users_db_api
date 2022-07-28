from flask import Flask


def create_app(config_filename):
    app = Flask(__name__, static_folder="static")

    app.config.from_object(config_filename)

    from app.models import db
    db.init_app(app)

    return app
