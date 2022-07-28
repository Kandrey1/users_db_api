from flask import redirect, url_for
from app import create_app
from config import Config

app = create_app(Config)

client = app.test_client()


from app.models import db


@app.before_first_request
def create_table():
    db.create_all()


from app.api.blueprint import api_bp
from app.user.blueprint import user_bp

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(api_bp, url_prefix='/')


@app.route("/")
def index():
    """ Представление главной страницы """
    return redirect(url_for('user.user'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
