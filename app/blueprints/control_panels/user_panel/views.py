import os

from flask import abort, Blueprint, redirect, render_template, send_file, url_for
from flask_login import current_user, login_required

from app.extensions.logger import logger
from app.models import Finance

# Создание blueprint для пользовательской панели
blueprint = Blueprint('user_panel', __name__)

# Абсолютный путь к корню приложения (где находится папка app)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# Путь к папке acts
ACTS_DIRECTORY = os.path.join(BASE_DIR, 'static', 'acts')


@blueprint.route('/user/<int:area>')
@login_required
def user_panel(area):
    """
    Генерация страницы пользователя. Проверяется доступ к указанному участку.
    """
    try:
        logger.info(f"Пользователь {current_user.area_number} пытается получить доступ к странице участка {area}.")

        # Проверка прав доступа пользователя к указанному участку
        if current_user.area_number == area or current_user.is_admin:
            try:
                info = Finance.query.filter(Finance.area_number == area).first()
                if not info:
                    logger.warning(f"Данные по участку {area} отсутствуют.")
            except AttributeError:
                logger.warning(f"Ошибка при запросе данных для участка {area}.")
                info = None

            title = f'Личный кабинет участка {area}'
            logger.info(f"Страница доступна для пользователя {current_user.area_number}.")
            return render_template(
                'control_panels/user_panel.html',
                page_title=title,
                area=area,
                info=info
            )

        # Если доступ запрещён (участок не совпадает и пользователь не администратор)
        logger.warning(f"Доступ к участку {area} запрещён для пользователя {current_user.area_number}. Перенаправление.")
        return redirect(url_for('user_panel.user_panel', area=current_user.area_number))

    except Exception as e:
        # Общая обработка ошибок для маршрута и рендер ошибки
        logger.error(f"Необработанная ошибка на странице пользователя: {str(e)}")
        return render_template('error.html', page_title='Ошибка'), 500


@blueprint.route('/download/act/<int:area>', methods=['GET'])
@login_required
def download_act(area):
    """
    Защищённый маршрут для скачивания акта сверки.
    Проверяется права доступа к участку.
    """
    try:
        logger.info(f"Запрос на скачивание акта сверки для участка {area} со стороны пользователя {current_user.area_number}.")

        # Проверка прав доступа
        if current_user.area_number != area and not current_user.is_admin:
            logger.warning(f"Пользователь {current_user.id} не имеет прав на участок {area}.")
            abort(403)  # Доступ запрещён

        # Формирование имени файла и пути к нему
        file_name = f'{area}.xls'
        file_path = os.path.join(ACTS_DIRECTORY, file_name)
        logger.info(f"Попытка доступа к файлу: {file_path}")

        # Проверка, существует ли файл
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_name} не найден в {ACTS_DIRECTORY}.")
            abort(404)  # Возврат ошибки 404

        # Отправка файла на скачивание
        logger.info(f"Акт сверки {file_name} отправляется пользователю {current_user.area_number}.")
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        # Общая обработка ошибок для маршрута и рендер ошибки
        logger.error(f"Необработанная ошибка при скачивании акта: {str(e)}")
        return render_template('error.html', page_title='Ошибка'), 500
