from flask import Blueprint, render_template, request, flash
from ..models import db, User
from sqlalchemy.exc import IntegrityError
from ..api.controllers import SetParameter

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


@user_bp.route("/parameter", methods=["POST", "GET"], endpoint='parameter')
def parameter():
    """ Представления для страницы Parameters """
    context = dict()
    context['title'] = 'Parameter'
    context['users'] = User.query.all()

    if request.method == "POST":
        try:
            if 'add_parameter' in request.form:
                name = request.form.get('name_p')
                type = request.form.get('type_p')
                value = request.form.get('value_p')
                user_id = request.form.get('case__user')

                new_param = {'name': name, 'type_p': type, 'value': value}

                SetParameter().set(user_id=int(user_id), param=new_param)

        except Exception as e:
            flash(f"Ошибка. <{e}> ")

    return render_template("user/parameter.html", context=context)
