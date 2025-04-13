from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.blueprints.control_panels.admin_panel.forms import NewsForm, UploadFileForm
from app.extensions import db
from app.extensions.logger import logger
from app.models import News
from app.services.loader import insert_finance_data_db
from app.services.parsing_csv import parsing_csv


blueprint = Blueprint('admin_panel', __name__)


def handle_file_upload(form: UploadFileForm):
    """Обрабатывает загрузку CSV-файла и добавляет данные в БД."""
    try:
        logger.info('Загружается и обрабатывается CSV-файл.')
        csv_file = form.convert_file_field_data_to_csv_file()  # Преобразуем файл
        values_to_db = parsing_csv(csv_file)  # Парсим содержимое
        insert_finance_data_db(values_to_db)  # Загрузка данных в БД

        logger.info('CSV-файл успешно загружен, данные добавлены в БД.')
        flash('Данные успешно загружены.', 'success')
    except Exception as e:
        logger.error(f"Ошибка при обработке CSV-файла: {str(e)}")
        flash(f"Ошибка при загрузке данных: {str(e)}", 'error')


def handle_news_submission(form: NewsForm):
    """Обрабатывает создание и сохранение новостей в БД."""
    try:
        logger.info('Обрабатывается создание новой новости.')
        news_title = form.news_title.data
        news_content = form.news_content.data
        new_news = News(
            published=datetime.now(timezone.utc),
            text=news_content,
            title=news_title,
        )
        db.session.add(new_news)
        db.session.commit()  # Сохраняем изменения
        logger.info(f"Новость '{news_title}' успешно добавлена.")
        flash('Новость успешно опубликована.', 'success')
    except Exception as e:
        logger.error(f"Ошибка при добавлении новости: {str(e)}")
        db.session.rollback()  # Откатываем изменения в случае ошибки
        flash(f"Ошибка при добавлении новости: {str(e)}", 'error')


@blueprint.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    """
    Функция для обработки запросов на админ-странице.
    Обрабатывает загрузку файлов и создание новостей.
    """
    try:
        if not current_user.is_admin:
            # Если пользователь не администратор, перенаправляем на страницу логина
            logger.warning(f"Пользователь {current_user.area_number} попытался получить доступ к админ-панели.")
            return redirect(url_for('auth.login.login'))

        logger.info(f"Админ {current_user.area_number} открыл страницу админ-панели.")
        title = 'Страница Правления'

        form = UploadFileForm()
        news_form = NewsForm()

        # Проверяем действия на форме
        if form.submit.data and form.validate_on_submit():
            handle_file_upload(form)

        if news_form.submit.data and news_form.validate_on_submit():
            handle_news_submission(news_form)

        # Рендерим страничку
        return render_template('control_panels/admin_panel.html', a=form, b=news_form, page_title=title)

    except Exception as e:
        # Общая обработка ошибок для маршрута
        logger.error(f"Необработанная ошибка на странице админ-панели: {str(e)}")
        return render_template('error.html', page_title='Ошибка'), 500
