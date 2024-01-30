from io import StringIO
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from webapp.user.forms import LoginForm
from webapp.lk.models import FinancialData
from webapp.lk.forms import UploadFileForm
from webapp.lk.parsing_csv import parsing_csv

blueprint = Blueprint('lk', __name__)


@blueprint.route('/user/<int:area>')
def lk_page(area):
    """ Функция генерирующая страницу рядового пользователя.
     Также проверяет залогинен ли пользователь """
    if current_user.is_authenticated:
        if current_user.area_number == area or current_user.is_admin:
            info = FinancialData.query.filter(FinancialData.area_number == area).first()
            title = f'ЛК участка {area}'
            return render_template('lk/lk_page.html', page_title=title, area=area,
                                   member_fee=info.member_fee, targeted_fee=info.targeted_fee,
                                   electricity_payments=info.electricity_payments,
                                   published=info.published)
        return redirect(url_for('lk.lk_page', area=current_user.area_number))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@blueprint.route('/board_office', methods=['GET', 'POST'])
def board_office():
    """ Функция, отвечающая за страницу Правления(админ-страница). Предает в функцию рендеринга
      ФОРМУ загрузки файла, а также макет админ-страницы. Обрабатывает приходящий файл  """
    if current_user.is_admin:
        form = UploadFileForm()
        title = 'Страница Правления'
        if form.validate_on_submit():
            f = form.file.data
            text_from_csv = f.read().decode('cp1251')
            data = StringIO(text_from_csv)
            our_dict = parsing_csv(data)
            key_sort = list(sorted(our_dict))
            for k in key_sort:
                print(f'КЛЮЧ {k}: {our_dict[k]}')
            return render_template('lk/board_office.html', a=form, page_title=title)
        return render_template('lk/board_office.html', a=form, page_title=title)
    return redirect(url_for('lk.lk_page', area=current_user.area_number))
