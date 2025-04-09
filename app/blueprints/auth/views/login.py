from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.blueprints.auth.forms import LoginForm
from app.blueprints.auth.models import User

blueprint = Blueprint('login', __name__)


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
            return redirect(url_for('auth.login.login'))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.is_admin:
                return redirect(url_for('admin_panel.admin_panel'))
            return redirect(url_for('user_panel.user_panel', area=form.area_number.data))
    flash('Неверный номер участка или пароль')
    return redirect(url_for('auth.login.login'))

