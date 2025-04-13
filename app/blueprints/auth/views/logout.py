from app.extensions.logger import logger
from flask import Blueprint, flash, redirect, url_for
from flask_login import logout_user

blueprint = Blueprint('logout', __name__)


@blueprint.route('/logout')
def logout():
    """ Функция разлогинивания пользователя. Осуществляет выход их ЛК """
    try:
        logout_user()
        logger.info('Выход пользователя из личного кабинета')
        flash('Вы вышли из личного кабинета')
        return redirect(url_for('main_page.main_page'))
    except Exception as e:
        # Логируем ошибку при попытке разлогинить пользователя
        logger.error(f'Ошибка при выходе из личного кабинета: {str(e)}')
        return redirect(url_for('main_page.main_page')), 500

