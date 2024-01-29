from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from webapp.user.forms import LoginForm
from webapp.board_office.models import FinancialData

blueprint = Blueprint('lk', __name__)

@blueprint.route('/user/<int:area>')
def lk_page(area):
    """ Функция генерирующая страницу рядового пользователя.
     Также проверяет залогинен ли пользователь """

    if current_user.is_authenticated:
        if current_user.area_number == 0:
            return redirect(url_for('board_office.board_office'))

        info = FinancialData.query.filter(FinancialData.area_number == area).first()
        title = f'ЛК участка {area}'
        return render_template('lk_page.html', page_title=title, area=area,
                               member_fee=info.member_fee, targeted_fee=info.targeted_fee,
                               electricity_payments=info.electricity_payments,
                               published=info.published)
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)