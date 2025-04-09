from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.user.forms import RegistrationForm, LoginForm
from app.user.models import User
from app.db import db

blueprint = Blueprint('user', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Функция, отвечающая за страницу логина. Проверяет залогинен ли пользователь.
    Если да, то возвращает на главную страницу. Если нет, то передает в функцию рендеринга
    макет страницы логина, ФОРМУ логина, а также название страницы. В самой странице, при
    получении данных из формы они перенаправляются функции process_login """
    if current_user.is_authenticated:
        if current_user.area_number == 0:
            return redirect(url_for('admin_panel.admin_panel'))
        return redirect(url_for('user_panel.user_panel', area=current_user.area_number))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login/login.html', page_title=title, form=login_form)


@blueprint.route('/process_login', methods=['POST'])
def process_login():
    """ Функция обработки данных, перенаправленных со страницы логина. Проверяет,
     корректны ли данные, поступившие со страницы логина. Если нет, отправляет обратно
     на страницу логина. Если да, то проверяет, совпадает ли пароль пользователя с паролем в БД.
     В случае успеха перенаправляет на страницу ЛК админа. """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.area_number == form.area_number.data).first()
        if not user:
            flash('Пользователь с таким номером участка не зарегистрирован')
            return redirect(url_for('user.login'))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.is_admin:
                return redirect(url_for('admin_panel.admin_panel'))
            return redirect(url_for('user_panel.user_panel', area=form.area_number.data))
    flash('Неверный номер участка или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    """ Функция разлогинивания пользователя. Осуществляет выход их ЛК"""
    logout_user()
    flash('Вы вышли из личного кабинета')
    return redirect(url_for('news.index'))


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
            return redirect(url_for('user.registration'))
        new_user = User(area_number=form.area_number.data,
                        email=form.email.data,
                        phone=form.phone.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы зарегистрированы')
        return redirect(url_for('user.login'))
    else:

        error_lst = [''.join(err_value).lower() for err_value in form.errors.values()]
        error_str = ', '.join(error_lst)

        flash(f'Введены некорректные данные: {error_str}')
        return redirect(url_for('user.registration'))
