from flask import Blueprint, render_template, redirect, url_for
from flask import send_file, abort
from flask_login import current_user
from app.blueprints.auth.forms import LoginForm
from app.models import Finance
import os

blueprint = Blueprint('user_panel', __name__)

# Абсолютный путь к корню приложения (где находится папка app)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# Путь к папке acts
ACTS_DIRECTORY = os.path.join(BASE_DIR, 'static', 'acts')


@blueprint.route('/user/<int:area>')
def user_panel(area):
    """Функция генерирующая страницу рядового пользователя.
    Также проверяет залогинен ли пользователь."""
    print(f"ACTS_DIRECTORY: {ACTS_DIRECTORY}")

    if current_user.is_authenticated:
        if current_user.area_number == area or current_user.is_admin:  # Проверка прав доступа
            try:
                info = Finance.query.filter(Finance.area_number == area).first()
            except AttributeError:
                info = None
            title = f'ЛК участка {area}'
            return render_template('control_panels/user_panel.html', page_title=title,
                                   area=area, info=info)
        return redirect(url_for('user_panel.user_panel', area=current_user.area_number))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login/login.html', page_title=title, form=login_form)


@blueprint.route('/download/act/<int:area>', methods=['GET'])
def download_act(area):
    """
    Защищённый маршрут для скачивания акта сверки.
    """

    print(f"ACTS_DIRECTORY: {ACTS_DIRECTORY}")

    if not current_user.is_authenticated:
        abort(403)  # Если пользователь не авторизован, доступ запрещён
    if current_user.area_number != area and not current_user.is_admin:
        abort(403)  # Пользователь не имеет прав на доступ к данному участку

    file_name = f'{area}.xls'  # Имя файла на основе номера участка
    file_path = os.path.join(ACTS_DIRECTORY, file_name)
    print(f"ACTS_DIRECTORY: {ACTS_DIRECTORY}")
    print(f"file_path: {file_path}")

    if not os.path.exists(file_path):  # Проверка существования файла
        abort(404)  # Если файл не найден, возвращается ошибка 404

    return send_file(file_path, as_attachment=True)  # Отправка файла на скачивание
