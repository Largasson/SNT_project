from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.blueprints.auth.forms import LoginForm
from app.blueprints.control_panels.admin_panel.models import FinancialData

blueprint = Blueprint('user_panel', __name__)


@blueprint.route('/user/<int:area>')
def user_panel(area):
    """ Функция генерирующая страницу рядового пользователя.
     Также проверяет залогинен ли пользователь """
    if current_user.is_authenticated:
        if current_user.area_number == area or current_user.is_admin:
            try:
                info = FinancialData.query.filter(FinancialData.area_number == area).first()
            except AttributeError:
                info = None
                # log_info(f'Проблемы с получением финансовой информации: {err}')
            title = f'ЛК участка {area}'
            return render_template('control_panels/user_panel.html', page_title=title,
                                   area=area, info=info)
        return redirect(url_for('control_panel.user_panel', area=current_user.area_number))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)
