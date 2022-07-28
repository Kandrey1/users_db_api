from flask import Blueprint, render_template, request, flash
from ..models import db, User
from sqlalchemy.exc import IntegrityError


user_bp = Blueprint('user', __name__)


@user_bp.route("/", methods=["POST", "GET"], endpoint='user')
def user():
    """ Представления для страницы USER
        (redirect с главной на нее происходит)
    """
    context = dict()
    context['title'] = 'User'

    if request.method == "POST":
        try:
            if 'show_user' in request.form:
                context['users'] = User.query.all()
            if 'add_user' in request.form:
                input_user = request.form.get('user')

                user = User(name=input_user)
                db.session.add(user)
                db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            flash(f" User с именем <{input_user}> уже есть в БД ")

    return render_template("user/user.html", context=context)
