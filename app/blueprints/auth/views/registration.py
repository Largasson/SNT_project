from flask import Blueprint, render_template, flash, redirect, url_for
from app.blueprints.auth.forms import RegistrationForm
from app.blueprints.auth.models import User
from app.db import db

blueprint = Blueprint('registration', __name__)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    """ Функция, отвечающая за страницу регистрации"""
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('login/registration.html', page_title=title, form=registration_form)


@blueprint.route('/reg_processing', methods=['POST'])
def reg_processing():
    """ Функция перехвата данных со страницы регистрации. Если данные валидны,
    то добавляются в ЮД пользователей, в противном случае пользователь
    перенаправляется на страницу регистрации"""
    users = [x.area_number for x in db.session.query(User.area_number).distinct()]
    form = RegistrationForm()
    if form.validate_on_submit():
        if int(form.area_number.data) in users:
            flash('Пользователь с таким номером участка уже зарегистрирован')
            return redirect(url_for('auth.registration.registration'))
        new_user = User(area_number=form.area_number.data,
                        email=form.email.data,
                        phone=form.phone.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы зарегистрированы')
        return redirect(url_for('auth.login.login'))
    else:

        error_lst = [''.join(err_value).lower() for err_value in form.errors.values()]
        error_str = ', '.join(error_lst)

        flash(f'Введены некорректные данные: {error_str}')
        return redirect(url_for('auth.registration.registration'))
