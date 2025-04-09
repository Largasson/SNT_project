from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app import db
from app.blueprints.news.models import News
from app.user.forms import LoginForm
from app.blueprints.control_panels.admin_panel.models import FinancialData
from app.blueprints.control_panels.admin_panel.forms import UploadFileForm, NewsForm
from app.parsing_csv import parsing_csv
from app.loader import insert_finance_data_db
from datetime import datetime


blueprint = Blueprint('admin_panel', __name__)


@blueprint.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    """ Функция, отвечающая за страницу Правления(админ-страница). Предает в функцию рендеринга
      ФОРМУ загрузки файла, а также макет админ-страницы. Обрабатывает приходящий файл  """
    if current_user.is_admin:
        form = UploadFileForm()
        news_form = NewsForm()
        title = 'Страница Правления'
        if form.submit1.data and form.validate_on_submit():
            csv_file = form.convert_file_field_data_to_csv_file()
            values_to_db = parsing_csv(csv_file)
            insert_finance_data_db(values_to_db)
            ''' Логирование распарсеных данных. Нужно для контроля входящего файла '''
            # key_sort = list(sorted(values_to_db))
            # for k in key_sort:
            #     log_info(f'КЛЮЧ {k}: {values_to_db[k]}')
        if news_form.submit2.data and news_form.validate_on_submit():
            news_title = news_form.news_title.data
            news_content = news_form.news_content.data
            new_news = News(published=datetime.utcnow(), text=news_content, title=news_title)
            db.session.add(new_news)
            db.session.commit()
        return render_template('control_panels/admin_panel.html', a=form, b=news_form, page_title=title)
    return redirect(url_for('control_panel.admin_panel', area=current_user.area_number))
