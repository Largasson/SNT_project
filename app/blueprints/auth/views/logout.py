from flask import Blueprint, flash, redirect, url_for
from flask_login import logout_user

blueprint = Blueprint('logout', __name__)


@blueprint.route('/logout')
def logout():
    """ Функция разлогинивания пользователя. Осуществляет выход их ЛК"""
    logout_user()
    flash('Вы вышли из личного кабинета')
    return redirect(url_for('news.index'))
